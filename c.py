from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.util import path_expand


d = ConfigDict("cloudmesh.yaml", verbose=True)

os_password = d["cloudmesh.clouds.chameleon.credentials.OS_PASSWORD"]
os_username = d["cloudmesh.clouds.chameleon.credentials.OS_USERNAME"]

print os_username, os_password

driver = webdriver.Firefox()

from pprint import pprint

pprint (driver.profile.__dict__)

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", path_expand('~/.cloudmesh/'))
driver = webdriver.Firefox(firefox_profile=profile)

driver.get("https://openstack.tacc.chameleoncloud.org/dashboard/project/")
username = driver.find_element_by_name("username")
username.send_keys(os_username)

username = driver.find_element_by_name("password")
username.send_keys(os_password)

driver.find_element_by_id("loginBtn").click()

driver.get("https://openstack.tacc.chameleoncloud.org/dashboard/project/access_and_security/api_access/openrc/")


element = webdriver.WebDriverWait(driver, 10)

driver.close()


#assert "Python" in driver.title
#elem = driver.find_element_by_name("q")
#elem.send_keys("pycon")
#elem.send_keys(Keys.RETURN)
#assert "No results found." not in driver.page_source
#driver.close()
