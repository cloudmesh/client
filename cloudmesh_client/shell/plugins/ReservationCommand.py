import pprint
import json
from cloudmesh_client.common.tables import dict_printer

from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.cm import command
from cloudmesh_client.common.todo import TODO


class ReservationCommand(object):
    topics = {"register": "hpc"}

    def __init__(self, context):
        # super(self.__class__, self).__init__()
        self.context = context
        if self.context.debug:
            print("init command reservation")

    @command
    def do_reservation(self, args, arguments):
        """
        ::

            Usage:
                reservation info [--user=USER]
                                 [--project=PROJECT]
                reservation list [--user=USER]
                                 [--project=PROJECT]
                                 [--name=NAMES]
                                 [--start=TIME_START]
                                 [--end=TIME_END]
                                 [--host=HOST]
                                 [--format=FORMAT]
                reservation delete [all]
                                   [--user=USER]
                                   [--project=PROJECT]
                                   [--name=NAMES]
                                   [--start=TIME_START]
                                   [--end=TIME_END]
                                   [--host=HOST]
                reservation delete --file=FILE
                reservation update [--name=NAMES]
                                   [--start=TIME_START]
                                   [--end=TIME_END]
                reservation add [--user=USER]
                                [--project=PROJECT]
                                [--host=HOST]
                                [--description=DESCRIPTION]
                                --name=NAMES
                                --start=TIME_START
                                --end=TIME_END
                reservation add --file=FILE

            Options:
                --name=NAMEs          Names of the reservation
                --user=USER           user name
                --project=PROJECT     project id
                --start=TIME_START    Start time of the reservation, in
                                      YYYY/MM/DD HH:MM:SS format. [default: 1901-01-01]
                --end=TIME_END        End time of the reservation, in
                                      YYYY/MM/DD HH:MM:SS format. In addition a duration
                                      can be specified if the + sign is the first sign.
                                      The duration will than be added to
                                      the start time. [default: 2100-12-31]
                --host=HOST           host name
                --description=DESCRIPTION  description summary of the reservation
                --file=FILE           Adding multiple reservations from one file
                --format=FORMAT       Format is either table, json, yaml or csv
                                      [default: table]

            Description:

                reservation info
                    lists the resources that support reservation for
                    a given user or project. 
        """

        # print (arguments)

        if (arguments["list"]):
            """
            db = Reservation()
            reservations = db.list(cm_id=arguments["--cm_id"],
                                   user=arguments["--user"],
                                   project=arguments["--project"],
                                   label= arguments["--label"],
                                   start_time= arguments["--start"],
                                   end_time=arguments["--end"],
                                   host=arguments["--host"],
                                   summary=arguments["--summary"])
            _print_reservations(reservations, arguments["--format"])
            """
            TODO("implement")

        elif (arguments["find"]):
            """
            db = Reservation()

            if(arguments["all"]):
                reservations = db.find_all()
            elif(arguments["--user"]):
                reservations = db.find_user(arguments["--user"])
            elif(arguments["--label"]):
                reservations = db.find_label(arguments["--label"])
            elif(arguments["--cm_id"]):
                reservations = db.find_id(arguments["--cm_id"])
            else:
                reservations = db.find_all()

            _print_reservations(reservations, arguments["--format"])
            """
            TODO("implement")
        elif (arguments["duration"]):
            """
            db = Reservation()
            print db.duration(arguments["--cm_id"])
            """
            TODO("implement")
        elif (arguments["delete"]):
            if (arguments["all"]):
                """
                db = Reservation()
                db.delete_all()
                """
                TODO("implement")
            else:
                TOTO("implement")
                """
                db = Reservation()
                db.delete_selection(cm_id=arguments["--cm_id"],
                                              user=arguments["--user"],
                                              project=arguments["--project"],
                                              label= arguments["--label"],
                                              start_time= arguments["--start"],
                                              end_time=arguments["--end"],
                                              host=arguments["--host"])
                """
        elif (arguments["add"]):

            if arguments["--file"] is None:

                TODO("implement")
                """
                db = Reservation(label=arguments["--label"],
                                 user=arguments["--user"],
                                 project=arguments["--project"],
                                 start_time=arguments["--start"],
                                 end_time=arguments["--end"],
                                 cm_id=arguments["--cm_id"],
                                 host=arguments["--host"],
                                 summary=arguments["--summary"])
                db.add()
                """
            else:
                try:
                    TODO("implement")
                    """
                    with open(os.path.join(sys.path[0], arguments["--file"])) as file:
                        reader = csv.reader(file)
                        for row in reader:
                            reservations = Reservation(cm_id=row[0],
                                                    label=row[1],
                                                    user=row[2],
                                                    project=row[3],
                                                    start_time=row[4],
                                                    end_time=row[5],
                                                    host=row[6],
                                                    summary=row[7])
                            db.add()
                    """
                except Exception as e:
                    print "Error in adding from file. ", e

    '''
        elif(arguments["update"]):
              reservations = Reservation()
              fromObj = [str(sys.argv[2]).split("=")[0].replace("--", ""),str(sys.argv[2]).split("=")[1]]
              toObj = [str(sys.argv[3]).split("=")[0].replace("--", ""),str(sys.argv[3]).split("=")[1]]
              fromBody = {cm_id=101, project = 20, user = "oliver"}
              toBody = {cm_id=101, project = 20, user = "oliver"}
              db.update_selection(cm_id=fromObj[1],project=toObj[1])
              print db.find_all()
    '''
