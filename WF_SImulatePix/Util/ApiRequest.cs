using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using WF_SImulatePix.Util.Classes;

namespace WF_SImulatePix.Util
{
    class ApiRequest
    {
        public string[] createAccount(JObject json)
        {
            try
            {
                HttpClient http = new HttpClient();
                var result = http.PostAsJsonAsync(@"http://127.0.0.1:5000/createAccount", json).Result;
                if (result.IsSuccessStatusCode)
                {
                    string[] returnSuccess = new string[1] { result.Content.ReadAsStringAsync().Result };
                    return returnSuccess;
                }
                else
                {
                    ApiMessage returnApi = JsonConvert.DeserializeObject<ApiMessage>(result.Content.ReadAsStringAsync().Result);
                    string[] returnError = new string[2] { returnApi.message, result.StatusCode.ToString() };
                    return returnError;
                }
            }
            catch (Exception ex)
            {
                throw ex;
            }
        }

        public string[] loginAccount(JObject json)
        {
            try
            {
                HttpClient http = new HttpClient();
                var result = http.PostAsJsonAsync(@"http://127.0.0.1:5000/login", json).Result;
                if (result.IsSuccessStatusCode)
                {
                    string[] returnSuccess = new string[1] { result.Content.ReadAsStringAsync().Result };
                    return returnSuccess;
                }
                else
                {
                    ApiMessage error = new ApiMessage();
                    error = JsonConvert.DeserializeObject<ApiMessage>(result.Content.ReadAsStringAsync().Result);
                    string[] returnError = new string[2] { error.message, result.StatusCode.ToString() };
                    return returnError;
                }
            }catch(Exception ex)
            {
                throw ex;
            }
        }

       public string[] sendPix(JObject json, string token, string secureToken)
        {
            try
            {
                HttpClient http = new HttpClient();
                //http.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
                //http.DefaultRequestHeaders.Add("Bearer", token);
                http.DefaultRequestHeaders.Add("secureToken", secureToken);
                http.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
                var result = http.PostAsJsonAsync(@"http://127.0.0.1:5000/pix", json).Result;
                if (result.IsSuccessStatusCode)
                {
                    string[] returnSuccess = new string[1] { result.Content.ReadAsStringAsync().Result };
                    return returnSuccess;
                }
                else
                {
                    ApiMessage error = new ApiMessage();
                    error = JsonConvert.DeserializeObject<ApiMessage>(result.Content.ReadAsStringAsync().Result);
                    string[] returnError = new string[2] { error.message, result.StatusCode.ToString() };
                    return returnError;
                }
            }
            catch(Exception ex)
            {
                throw ex;
            }
        }

        public string[] deleteAccount(JObject json, string token, string secureToken)
        {
            try
            {
                HttpClient http = new HttpClient();
                http.DefaultRequestHeaders.Add("secureToken", secureToken);
                http.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
                var result = http.PostAsJsonAsync(@"http://127.0.0.1:5000/del", json).Result;
                ApiMessage msg = JsonConvert.DeserializeObject<ApiMessage>(result.Content.ReadAsStringAsync().Result);
                string[] returnError = new string[2] { msg.message, result.StatusCode.ToString() };
                return returnError;
            }
            catch(Exception ex)
            {
                throw ex;
            }
        }
    }
}
