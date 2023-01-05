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

        with open(devices[device_obj]["bgp_conf_file"]) as json_file:
            data = json.load(json_file)
            print(type(data))
            print(data)
            print
        
        print("Configure bgp for {} with asn {} and neighbor {}".format(devices[device_obj]["address"], data["bgp_config"]["asn"], data["bgp_config"]["peer-list"]["peer1"]))
        asn = data["bgp_config"]["asn"]
        rtrId = data["bgp_config"]["rtrId"]
        DomAf = data["bgp_config"]["Dom-Af"]
        prefix = data["bgp_config"]["prefix-list"]["prefix"]
        peer = data["bgp_config"]["peer-list"]["peer1"]
        neighbor_asn = data["bgp_config"]["peer-list"]["asn"]
        neighbor_af = data["bgp_config"]["peer-list"]["address-family"]
        bgp_config = """
        <config>
        <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
        <bgp-items>
            <inst-items>
                <asn> {asn}</asn>
                <dom-items>
                    <Dom-list>
                        <name>default</name>
                        <rtrId>{rtrId}</rtrId>
                        <af-items>
                            <DomAf-list>
                                <type>{DomAf}</type>
                                <prefix-items>
                                    <AdvPrefix-list>
                                        
                                        <addr>{prefix}</addr>
                                    </AdvPrefix-list>
                                </prefix-items>
                            </DomAf-list>
                        </af-items>
                        <peer-items>
                            <Peer-list>
                                <addr> {neighbor}</addr>
                                <asn>{neighbor_asn}</asn>
                                <af-items>
                                    <PeerAf-list>
                                        <type>{neighbor_af}</type>
                                    </PeerAf-list>
                                </af-items>
                            </Peer-list>
                        </peer-items>
                    </Dom-list>
                </dom-items>
            </inst-items>
        </bgp-items>
        </System>
        </config>""".format(asn=asn, rtrId=rtrId, DomAf= DomAf, prefix= prefix, neighbor = peer, neighbor_asn= neighbor_asn, neighbor_af=neighbor_af)
        print(bgp_config)
        with manager.connect(host = devices[device_obj]["address"],
                         port = devices[device_obj]["netconf_port"],
                         username = devices[device_obj]["username"],
                         password = devices[device_obj]["password"],
                         hostkey_verify = False) as m:
            netconf_response = m.edit_config(target='running', config=bgp_config)
            # Parse the XML response
            print(netconf_response)


if __name__ == '__main__':
    sys.exit(main())
