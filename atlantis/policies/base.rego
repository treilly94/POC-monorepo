package main

import rego.v1

denylist := ["random_string"]

deny contains msg if {
	startswith(input.resource_changes[_].type, denylist[_])
	banned := concat(", ", denylist)
	msg := sprintf("Terraform plan will change prohibited resources in the following namespaces: %v", [banned])
}
