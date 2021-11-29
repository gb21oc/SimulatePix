using Newtonsoft.Json;
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
    public partial class WF_CreateAccount : Form
    {
        public WF_CreateAccount()
        {
            InitializeComponent();
        }

        private void btnUndo_Click(object sender, EventArgs e)
        {
            mskCpf.Text = "";
            txtPassword.Text = "";
            txtEmail.Text = "";
            txtFullName.Text = "";
        }

        private void btnRegister_Click(object sender, EventArgs e)
        {
            try
            {
                ApiRequest api = new ApiRequest();
                var data = "{\"cpf\": \"" + mskCpf.Text + "\", \"email\": \"" + txtEmail.Text + "\", \"password\": \"" + txtPassword.Text + "\", \"fullName\": \"" + txtFullName.Text + "\"}";
                JObject json = JObject.Parse(data);
                string[] result = api.createAccount(json);
                if (result.Length >= 2)
                {
                    // Retorno de Erro
                    //ApiMessage res = JsonConvert.DeserializeObject<ApiMessage>(result[0]); // Retornou tudo certo!
                    MessageBox.Show($"{result[0]}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                else
                {
                    // Retorno de sucesso
                    ApiMessage res = JsonConvert.DeserializeObject<ApiMessage>(result[0]); // Retornou tudo certo!
                    MessageBox.Show($"{res.message}", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    WF_Login loginAccount = new WF_Login();
                    loginAccount.Closed += (s, args) => this.Close();
                    loginAccount.Show();
                    Hide();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("An unexpected error has occurred", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void btnBack_Click(object sender, EventArgs e)
        {
            WF_Login loginAccount = new WF_Login();
            loginAccount.Closed += (s, args) => this.Close();
            loginAccount.Show();
            Hide();
        }
    }
}
