from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.factory import loadyaml

globals().update( loadyaml('flowsession.yml'))

dev = Device('10.10.1.1')
cu = Config(dev)

dev.open()
session_table = SessionTable(dev)
session_table.get()

for s in session_table:
  if session_table.keys():
    if s.session_direction == 'In' and s.destination_address == '192.168.0.105' and s.destination_port == '22' and s.session_protocol == 'tcp':
      block_src = {'Address': s.source_address}
      rsp = cu.load( template_path="add-global-address-book-template.conf", template_vars=block_src )
      clearflow = dev.rpc.clear_flow_session(destination_prefix=s.destination_address, source_prefix=s.source_address, destination_port=s.destination_port, protocol=s.session_protocol)
      cu.commit()

dev.close()
