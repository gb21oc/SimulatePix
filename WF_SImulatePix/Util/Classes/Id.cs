using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Text;

namespace WF_SImulatePix.Util.Classes
{
    public class Id
    {
        [JsonProperty("$oid")]
        public string Oid { get; set; }
    }
}
