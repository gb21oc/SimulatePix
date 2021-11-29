using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using WF_SImulatePix.Util;
using WF_SImulatePix.Util.Classes;

namespace WF_SImulatePix
{
    public partial class WF_Login : Form
    {
        /*
         -> History DEV:
            -> 20/11/2021: 1h
            -> 23/11/2021: 30M:40S
            -> 29/11/2021: 14M:34S
         */
        public WF_Login()
        {
            InitializeComponent();
        }

        private void login()
        {
            try
            {
                if (String.IsNullOrEmpty(mskCpf.Text.Trim()) || String.IsNullOrEmpty(txtPassword.Text.Trim()))
                {
                    MessageBox.Show("It is not possible to login with empty fields", "Error", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    return;
                }
                ApiRequest api = new ApiRequest();
                this.Cursor = Cursors.WaitCursor;
                var data = "{\"cpf\": \"" + mskCpf.Text + "\", \"password\": \"" + txtPassword.Text + "\"}";
                JObject json = JObject.Parse(data);
                var result = api.loginAccount(json);
                if (result.Length >= 2)
                {
                    // Retorno de Erro
                    MessageBox.Show($"{result[0]}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    this.Cursor = Cursors.Default;
                    return;
                }
                else
                {
                    // Retorno de sucesso
                    this.Cursor = Cursors.Default;
                    Response res = JsonConvert.DeserializeObject<Response>(result[0]); // Retornou tudo certo!
                    MessageBox.Show($"Login successfully", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    Pix px = new Pix(res);
                    px.Closed += (s, args) => this.Close();
                    px.Show();
                    Hide();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("An unexpected error has occurred", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
        }

        private void btnUndo_Click(object sender, EventArgs e)
        {
            mskCpf.Text = "";
            txtPassword.Text = "";
        }

        private void btnRegister_Click(object sender, EventArgs e)
        {
            if (String.IsNullOrEmpty(mskCpf.Text.Trim()) || String.IsNullOrEmpty(txtPassword.Text.Trim()))
            {
                WF_CreateAccount createAccount = new WF_CreateAccount();
                createAccount.Closed += (s, args) => this.Close();
                createAccount.Show();
                Hide();
            }
            else
            {
                MessageBox.Show("It is only possible to register with empty fields", "Error", MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }
            
        }

        private void btnLogin_Click(object sender, EventArgs e)
        {
            login();
        }

        private void txtPassword_KeyPress(object sender, KeyPressEventArgs e)
        {
            if(e.KeyChar == 13)
            {
                btnLogin.Enabled = false;
                 login();
            }
        }
    }
}
