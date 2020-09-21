
import WoS_Fields from "./query_wos_fields";
import MAG_Fields from "./query_mag_fields";

export default{
    "wos": {
        name: "Web of Science",
        fields: WoS_Fields,
        description: "Metadata for scholarly papers and their authors",
        allowed_roles: ["wos_gold", "wos_limited", "wos_trial"],
        database_type: "janus"
    },
    "mag": {
        name: "Microsoft Academic Graph",
        fields: MAG_Fields,
        description: "Metadata for scholarly papers and their authors",
        allowed_roles: [],
        database_type: "janus"
    }
}
