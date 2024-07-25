import Find_MAC_CSV
import Description_generator
import Connection_ssh_lldp_txt_v2
import Find_output_mv_to_dir
import Description_generator_compare


def main():
    Connection_ssh_lldp_txt_v2.main()
    Find_MAC_CSV.main()
    Description_generator.main()
    Find_output_mv_to_dir.main()
    Description_generator_compare.main()


if __name__ == "__main__":
    main()