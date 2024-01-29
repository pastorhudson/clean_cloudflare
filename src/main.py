import argparse
from utils import setup_logger, check_config
from clean import clean_videos, test_keys


def main():
    """
    Main function of the program.

    :return: None
    """
    logger = setup_logger(__name__)
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="test option: return the string 'SUCCESS'", action='store_true')
    # parser.add_argument("-s", "--service_type_id", help="service type id")
    # parser.add_argument("-p", "--plan_id", help="plan id")

    args = parser.parse_args()

    if args.test:
        try:
            check_config()
            test_keys()
        except Exception as e:
            logger.error(e)
        return
    else:
        try:
            clean_videos()
        except KeyboardInterrupt:
            logger.info("Thanks for using this recipe https://github.com/pastorhudson/clean_cloudflare.\n"
                        "Check out more recipes at https://pcochef.com")
        except Exception as e:
            logger.error(e)


if __name__ == "__main__":
    main()
