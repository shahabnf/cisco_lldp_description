import Find_MAC_CSV
import Description_generator
import Connection_ssh_lldp_txt_v2


def main():
    Connection_ssh_lldp_txt_v2.main()
    Find_MAC_CSV.main()
    Description_generator.main()


if __name__ == "__main__":
    main()