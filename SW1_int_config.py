################### NXOS INTERFACE CONFIG FILE ########################################
from ncclient import manager
import sys
from lxml import etree


import json

sys.path.append("..") # noqa

def main():
    """
    data = json.loads(Sw1_eth_IPs)
    print(data)
    print(type(data))
    print(data['ethernet1/1']['ip'])
    print("{} ---> {}".format(data['ethernet1/1']['id'], data['ethernet1/1']['ip']))
    print("{} ---> {}".format(data['ethernet1/2']['id'], data['ethernet1/2']['ip']))
    print(data['ethernet1/2']['ip'])
    data = json.loads(Sw2_eth_IPs)
    print(data)
    print(type(data))
    print(data['ethernet1/1']['ip'])
    print(data['ethernet1/2']['ip'])
    print("{} ---> {}".format(data['ethernet1/1']['id'], data['ethernet1/1']['ip']))
    print("{} ---> {}".format(data['ethernet1/2']['id'], data['ethernet1/2']['ip']))


    """   
    with open('devices.json') as devices_file:
        devices = json.load(devices_file)
        print(devices)

    for device_obj in devices:
        print(devices[device_obj])
        print(devices[device_obj]["address"])

        with open(devices[device_obj]["int_conf_file"]) as json_file:
            data = json.load(json_file)
            print(type(data))
            print(data)
            #print(data["Sw1_Ethernet1/1"]["ip"])
        for interface_obj in data:
            print("Config for Device {} for interface {} with IP address {}".format(devices[device_obj]["address"], data[interface_obj]["id"], data[interface_obj]["ip"]))
            add_ip_interface = """<config>
    <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
        <intf-items>
            <phys-items>
                <PhysIf-list>
                    <id>{id}</id>
                    <adminSt>up</adminSt>
                    <layer>Layer3</layer>
                    <descr>Full intf config via NETCONF</descr>
                </PhysIf-list>
            </phys-items>
        </intf-items>
        <ipv4-items>
            <inst-items>
                <dom-items>
                    <Dom-list>
                        <name>default</name>
                        <if-items>
                            <If-list>
                                <id>{id}</id>
                                <addr-items>
                                    <Addr-list>
                                        <addr>{ip}</addr>
                                    </Addr-list>
                                </addr-items>
                            </If-list>
                        </if-items>
                    </Dom-list>
                </dom-items>
            </inst-items>
        </ipv4-items>
    </System>
    </config>""".format(id = data[interface_obj]["id"], ip = data[interface_obj]["ip"])
            print(add_ip_interface) 
            with manager.connect(host = devices[device_obj]["address"],
                         port = devices[device_obj]["netconf_port"],
                         username = devices[device_obj]["username"],
                         password = devices[device_obj]["password"],
                         hostkey_verify = False) as m:

        # Add the loopback interface
                print("Config for Device {} for interface {} with IP address {}".format(devices[device_obj]["address"], data[interface_obj]["id"], data[interface_obj]["ip"]))
                netconf_response = m.edit_config(target='running', config=add_ip_interface)
        # Parse the XML response
                print(netconf_response)

    
                    
        
        

if __name__ == '__main__':
    sys.exit(main())
