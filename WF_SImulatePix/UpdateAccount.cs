using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using WF_SImulatePix.Util;
using WF_SImulatePix.Util.Classes;

namespace WF_SImulatePix
{
    public partial class UpdateAccount : Form
    {
        // Create var
        string _token;
        string _cpf;
        string _name;
        string _email;
        string _account;
        string _randomKey;
        string _securetoken;
        Response _res;
        public UpdateAccount(Response res)
        {
            InitializeComponent();
            _token = res.token;
            _cpf = res.data.cpf;
            _name = res.data.name;
            _email = res.data.email;
            _account = res.data.account;
            _randomKey = res.data.randomKey;
            _securetoken = res.secureTokenUpdate;
            _res = res;
        }

        private void btnUndo_Click(object sender, EventArgs e)
        {
            txtFullName.Text = "";
            txtPassword.Text = "";
            txtEmail.Text = "";
        }

        private void btnUpdate_Click(object sender, EventArgs e)
        {
            try
            {
                if (txtEmail.Text == "" && txtFullName.Text == "")
                {
                    MessageBox.Show("To update your information, the \"FullName\" or \"Email\" field must be filled in", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }
                ApiRequest api = new ApiRequest();
                this.Cursor = Cursors.WaitCursor;
                var data = "";
                if (txtPassword.Text.Trim() != "")
                {
                    data = "{\"cpf\": \"" + _cpf + "\", \"password\":\"" + txtPassword.Text + "\", \"fullName\":\"" + txtFullName.Text + "\", \"account\":\"" + _account + "\", \"randomKey\":\"" + _randomKey + "\"}";
                }
                else
                {
                    data = "{\"cpf\": \"" + _cpf + "\", \"fullName\":\"" + txtFullName.Text + "\", \"account\":\"" + _account + "\", \"randomKey\":\"" + _randomKey + "\"}";
                }
                JObject json = JObject.Parse(data);
                var msg = api.updateAccount(json, _token, _securetoken);
                if (msg[1] != "OK")
                {
                    this.Cursor = Cursors.Default;
                    MessageBox.Show($"{msg[0]}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }
                else
                {
                    MessageBox.Show($"{msg[0]}", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    Pix pix = new Pix(_res);
                    pix.Close();
                    WF_Login loginAccount = new WF_Login();
                    loginAccount.Closed += (s, args) => this.Close();
                    loginAccount.Show();
                    Hide();
                }
            }
            catch(Exception ex)
            {
                this.Cursor = Cursors.Default;
                MessageBox.Show("An unexpected error has occurred", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
        }
    }
}
