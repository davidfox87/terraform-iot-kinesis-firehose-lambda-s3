locals {
  project_name = "awstimeseries"
  iot_topic    = "sensors"
}

variable "sonoff_id_list" {
  type        = list(string)
  description = "List of subscribers things deployed in AWS."
  default     = ["1", "2"]
}

variable "subscriber_group" {
  type        = string
  description = "Group of subscriber things"
  default     = "subscriber-app-group"
}