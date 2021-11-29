using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Text;
using System.Windows.Forms;
using WF_SImulatePix.Util;
using WF_SImulatePix.Util.Classes;

namespace WF_SImulatePix
{
    public partial class Pix : Form
    {

        // Create var
        string _token;
        string _cpf;
        string _name;
        string _email;
        int _balance;
        string _account;
        string _randomKey;
        string _securetoken;
        Response _res;
        public Pix(Response res)
        {
            InitializeComponent();
            // Create var
            _res = res;
            _token = res.token;
            _cpf = res.data.cpf;
            _name = res.data.name;
            _email = res.data.email;
            _balance = res.data.balance;
            _account = res.data.account;
            _randomKey = res.data.randomKey;
            _securetoken = res.secureTokenUpdate;

            // Setting label
            mskCpf.Text = _cpf;
            lblName.Text = _name;
            lblEmail.Text = _email;
            txtAgSender.Text = _account;
            lblBalance.Text = _balance.ToString();
            lblBalance.ForeColor = _balance < 100 ? Color.Red : Color.Green;
        }

        public void generatePdf(string pdf)
        {
            try 
            {
                SaveFileDialog sfd = new SaveFileDialog();
                sfd.DefaultExt = "pdf";
                sfd.Filter = "pdf files (*.pdf)|*.pdf|All files (*.*)|*.*";
                sfd.AddExtension = false;
                DialogResult result = sfd.ShowDialog();
                byte[] bytes = Convert.FromBase64String(pdf);
                System.IO.FileStream stream = new FileStream(@$"{sfd.FileName}", FileMode.CreateNew);
                System.IO.BinaryWriter writer = new BinaryWriter(stream);
                writer.Write(bytes, 0, bytes.Length);
                writer.Close();
                MessageBox.Show($@"File generated in path: {sfd.FileName}", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch(Exception ex)
            {
                throw ex;
            }
            
        }

        private void btnSend_Click(object sender, EventArgs e)
        {
            try
            {
                if (String.IsNullOrEmpty(txtPix.Text.Trim()) || String.IsNullOrEmpty(mskDestiny.Text.Trim()))
                {
                    MessageBox.Show("It is not possible to login with empty fields", "Error", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    return;
                }
                ApiRequest api = new ApiRequest();
                this.Cursor = Cursors.WaitCursor;
                var data = "{\"cpf\": \"" + mskCpf.Text + "\", \"randomKey\": \"" + _randomKey + "\", \"account_sender\": \"" + _account + "\", \"account_dst\": \"" + mskDestiny.Text + "\", \"pix\": \"" + txtPix.Text + "\"}";
                JObject json = JObject.Parse(data);
                var result = api.sendPix(json, _token, _securetoken);
                if (result.Length >= 2)
                {
                    // Retorno de Erro
                    MessageBox.Show($"{result[0]}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    this.Cursor = Cursors.Default;
                }
                else
                {
                    // Retorno de sucesso
                    this.Cursor = Cursors.Default;
                    SendPix res = JsonConvert.DeserializeObject<SendPix>(result[0]); // Retornou tudo certo!
                    generatePdf(res.pdf);
                    MessageBox.Show(res.message, "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    int newBalance = Convert.ToInt32(_balance) - Convert.ToInt32(txtPix.Text);
                    lblBalance.Text = newBalance.ToString();
                }
            }
            catch (Exception ex)
            {
                this.Cursor = Cursors.Default;
                MessageBox.Show("An unexpected error has occurred", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
        }

        private void btnUndo_Click(object sender, EventArgs e)
        {
            txtPix.Text = "";
            mskDestiny.Text = "";
        }

        private void txtPix_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (!Char.IsDigit(e.KeyChar) && e.KeyChar != (char)8)
            {
                e.Handled = true;
            }
        }

        private void btnUpdate_Click(object sender, EventArgs e)
        {
            UpdateAccount updateAccount = new UpdateAccount(_res);
            //updateAccount.MdiParent = this;
            updateAccount.Closed += (s, args) => this.Close();
            //updateAccount.ShowDialog();
            updateAccount.Show();
        }

        private void btnDelete_Click(object sender, EventArgs e)
        {
            try
            {
                DialogResult result = MessageBox.Show("Are you sure you want to delete your account?", "Confirmation", MessageBoxButtons.YesNo);
                if (result == DialogResult.Yes)
                {
                    ApiRequest api = new ApiRequest();
                    this.Cursor = Cursors.WaitCursor;
                    var data = "{\"cpf\": \"" + mskCpf.Text + "\", \"account\": \"" + _account + "\", \"randomKey\": \"" + _randomKey + "\"}";
                    JObject json = JObject.Parse(data);
                    var msg = api.deleteAccount(json, _token, _securetoken);
                    if (msg[1] != "OK")
                    {
                        MessageBox.Show($"{msg[0]}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        return;
                    }
                    else
                    {
                        MessageBox.Show($"{msg[0]}", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        WF_Login loginAccount = new WF_Login();
                        loginAccount.Closed += (s, args) => this.Close();
                        loginAccount.Show();
                        Hide();
                    }
                }
                else if (result == DialogResult.No)
                {
                    return;
                }
            }
            catch (Exception)
            {
                MessageBox.Show("An unexpected error has occurred", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
