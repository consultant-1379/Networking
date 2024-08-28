user's have two Directories /ansible & /results
your ansible directory will contain all your plays and a vlans.yml file
any results will be found in /results/<your ticket number>
the vlans.yml file must be edited before running the play in the following format:

---
networks:
  - name: <vlan name>
    tag: <vlan tag>
    subn: <ipv4 subnet including /2?>
    v6subn: <ipv6 subnet including /64>
  - name: <second vlan name>
    tag: <second vlan tag>

enter as many vlans as needed. if no subnet is needed on the vlan (example internal vlans)
leave out the subn: and v6subn: variables.

from inside your ansible directory run:
ansible-playbook <your play.yml>






