terraform {
  required_providers {
    twc = {
      source = "tf.timeweb.cloud/timeweb-cloud/timeweb-cloud"
    }
  }
  required_version = ">= 0.13"
}
###
data "twc_configurator" "example-configurator" {
  location = "pl-1"
}

data "twc_os" "example-os" {
  name    = "almalinux"
  version = "9.0"
}

data "twc_ssh_keys" "example-key" {
  name = "nvkmv@laptop"
}

# Select any preset from location = "ru-1", 10 Gb disk space with price between 50 and 100 RUB
data "twc_s3_preset" "example-s3-preset" {
  location = "ru-1"

  disk = 10 * 1024

  price_filter {
    from = 50
    to   = 100
  }
}

# Example private S3 bucket
resource "twc_s3_bucket" "example-s3-bucket" {
  name      = "example-s3-bucket"
  type      = "private"
  preset_id = data.twc_s3_preset.example-s3-preset.id
}
# machine
resource "twc_server" "s3" {
  name         = "Example server_s3"
  os_id        = data.twc_os.example-os.id
  ssh_keys_ids = [data.twc_ssh_keys.example-key.id]

  configuration {
    configurator_id = data.twc_configurator.example-configurator.id
    disk            = 40960
    cpu             = 2
    ram             = 2048
  }
}
