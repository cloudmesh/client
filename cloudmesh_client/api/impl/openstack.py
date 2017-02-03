from cloudmesh_client.cloud.network import Network

from cloudmesh_client.cloud.image import Image

from cloudmesh_client.cloud.vm import Vm

from cloudmesh_client import Console
from cloudmesh_client.api import Resource, Provider, Node

from cloudmesh_client.db.openstack.model import IMAGE_OPENSTACK, VM_OPENSTACK
from cloudmesh_client.common.util import exponential_backoff
from cloudmesh_client.default import Default


class ImageResource(Resource):
    def create(self):
        pass

    def delete(self):
        pass

    def list(self):
        pass

    def refresh(self):
        pass



class KeyResource(Resource):
    pass


class FloatingIpResource(Resource):
    pass


class FlavorResource(Resource):
    pass


class OpenstackProvider(Provider):

    # def __init__(self):
    #     super(OpenstackProvider, self).__init__()
    #
    #     self.images = ImageResource()
    #     self._add_resource(self.images)
    #
    #     self.keys = KeyResource()
    #     self._add_resource(self.keys)
    #
    #     self.flavors = FlavorResource()
    #     self._add_resource(self.flavors)
    #
    #     self.floating_ips = FloatingIpResource()
    #     self._add_resource(self.floating_ips)


    def boot(self, **kwargs):
        """Boot a single VM

        :param kwargs: parameters to :meth:`Vm.boot`
        :return: the vm details
        :rtype: :class:`Node`
        """

        cloud = kwargs.get('cloud', Default.cloud)
        name = kwargs.get('name', Vm.generate_vm_name())
        image = kwargs.get('image', Default.image)
        flavor = kwargs.get('flavor', Default.flavor)
        key = kwargs.get('key', Default.key)
        secgroup = kwargs.get('secgroup', Default.secgroup)
        group = kwargs.get('group', Default.group)
        username = kwargs.get('username', Image.guess_username(image))
        cluster = kwargs.get('cluster', None)

        # shorthand for getting a dict of all the vm details
        #
        # IMPORTANT: anything declared prior to the call to `locals()`
        # may be passed to `Vm.boot`, so make sure that only parameters are
        # defined above this comment.
        details = locals()
        details.pop('kwargs')

        # currently, Vm.boot returns the instance UUID from the provider for openstack images
        # 2016/12/12
        uuid = Vm.boot(**details)


        # helper function: the Vm.boot only returns a UUID, but we
        # need to use the VM model instead. Additionally, we'll need
        # to poll the VM to wait until it is active.
        #
        # The kwargs are used to select the item from the DB:
        # eg: uuid=???, cm_id=???, etc
        def get_vm(**kwargs):
            """Selects the VM based on the given properties"""
            model = self.db.vm_table_from_provider('openstack')
            vm = self.db.select(model, **kwargs).all()
            assert len(vm) == 1, vm
            vm = vm[0]
            return vm

        # get the VM from the UUID
        vm = get_vm(uuid=uuid)
        cm_id = vm.cm_id

        def is_active():
            Vm.refresh(cloud=cloud)
            vm = get_vm(cm_id=cm_id)
            return vm.status == 'ACTIVE'

        if not exponential_backoff(is_active):
            Console.error('Failed to get ACTIVE vm within timeframe')
            raise ValueError

        assert is_active()
        vm = get_vm(cm_id=cm_id)
        assert isinstance(vm, VM_OPENSTACK), vm.__class__

        return OpenstackNode(model=vm, provider=self)

    def create_ip(self, node):

        ip = Network.find_assign_floating_ip(
            cloudname=self.cloud,
            instance_id=node.name,
        )

        Vm.refresh(cloud=self.cloud)

        Console.ok('Assigned ip to {}: {}'.format(node.name, ip))

    def delete(self, nodde):
        raise NotImplementedError

    def node(self):
        raise NotImplementedError


class OpenstackNode(Node):

    def __init__(self, model, provider):
        super(Node, self).__init__()
        self._model = model
        self._provider = provider

    @property
    def name(self):
        return self._model.name

    @property
    def username(self):
        return self._model.username

    @property
    def private_ip(self):
        return self.model.static_ip

    @property
    def public_ip(self):
        return self.model.floating_ip

    def boot(self, **kwargs):
        pass

    def delete(self):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def ssh(self, cmd=None, user=None):
        raise NotImplementedError

    def create_ip(self):
        self._provider.create_ip(self)
