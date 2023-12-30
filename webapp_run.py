import gin
from google_data_transfer.ui.webapp import main

if __name__ == "__main__":
    gin.parse_config_file("config/local.gin")
    main()
