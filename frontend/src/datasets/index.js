
import WoS_Fields from "./query_wos_fields";
import MAG_Fields from "./query_mag_fields";
import WoS_2019_Fields from "./query_wos_2019_fields";

export default{
    "wos": {
        name: "Web of Science",
        fields: WoS_Fields,
        description: "Metadata for scholarly papers and their authors",
        allowed_roles: ["wos_gold", "wos_limited"]
    },
    "mag": {
        name: "Microsoft Academic Graph",
        fields: MAG_Fields,
        description: "Metadata for scholarly papers and their authors",
        allowed_roles: []
    },
    "wos_2019": {
        name: "Web of Science 2019",
        fields: WoS_2019_Fields,
        description: "2019 Collection of metadata for scholarly papers and their authors",
        allowed_roles: ["wos_gold", "wos_limited"]
    }
}
