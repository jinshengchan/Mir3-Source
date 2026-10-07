using Android.Views;
using Android.Widget;
using Client.Envir;
using System;
using C = Library.Network.ClientPackets;
namespace Mir3.Droid
{
    public partial class MainActivity
    {
        #region prop
        string _creatingAccount = "", _creatingPassword = "";
        public string CAccount
        {
            get => _creatingAccount;
            set
            {
                _creatingAccount = value ?? "";
                BeginInvoke(() =>
                {
                    var input = _newAccount?.FindViewById<EditText>(Resource.Id.c_acc);
                    if (input != null) input.Text = _creatingAccount;
                });
            }
        }

        public string CPwd
        {
            get => _creatingPassword;
            set
            {
                _creatingPassword = value ?? "";
                BeginInvoke(() =>
                {
                    var input = _newAccount?.FindViewById<EditText>(Resource.Id.c_pwd);
                    if (input != null) input.Text = _creatingPassword;
                });
            }
        }
        #endregion

        View _newAccount = null;

        private void ShowCreat()
        {
            _currentWindow = GetWindow(Resource.Layout.new_account);
            _newAccount = _currentWindow.ContentView;
            _creatingAccount = _creatingPassword = "";
            _newAccount.FindViewById<EditText>(Resource.Id.c_acc).TextChanged += (sender, args) => _creatingAccount = ((EditText)sender).Text ?? "";
            _newAccount.FindViewById<EditText>(Resource.Id.c_pwd).TextChanged += (sender, args) => _creatingPassword = ((EditText)sender).Text ?? "";
            var create = _newAccount.FindViewById<ImageButton>(Resource.Id.creat_btn);
            create.Click -= Create_Click;
            create.Click += Create_Click;
            var cancel = _newAccount.FindViewById<ImageButton>(Resource.Id.cancel_btn);
            cancel.Click -= Cancel_Click;
            cancel.Click += Cancel_Click;
            _currentWindow.ShowAtLocation(_overLayout, GravityFlags.CenterVertical, 0, 0);
        }

        private void Cancel_Click(object sender, EventArgs e)
        {
            _currentWindow.Dismiss();
        }

        private void Create_Click(object sender, EventArgs e)
        {
            if (_newAccount == null) return;
            var confirmation = _newAccount.FindViewById<EditText>(Resource.Id.c_pwd_confirm);
            if (string.IsNullOrWhiteSpace(CAccount) || string.IsNullOrEmpty(CPwd))
            {
                ShowMsg("请输入账号和密码。");
                return;
            }
            if (CPwd != confirmation.Text)
            {
                ShowMsg("两次输入的密码不一致。");
                return;
            }
            //var birthday = _newAccount.FindViewById<EditText>(Resource.Id.c_birthday);

            var inviteCode = _newAccount.FindViewById<EditText>(Resource.Id.c_invite_code);

            //var realName = _newAccount.FindViewById<EditText>(Resource.Id.c_real_name);


            //if(!DateTime.TryParse(birthday.Text, out DateTime birthDate))
            //{
            //    birthDate = new DateTime(1970, 1, 1);
            //}


            C.NewAccount packet = new C.NewAccount
            {
                EMailAddress = CAccount,
                Password = CPwd,
                InviteCode = inviteCode.Text,
                //RealName = realName.Text,
                //BirthDate = birthDate,
                Referral = "",
                CheckSum = CEnvir.C,
            };

            SubmitAccountRequest(packet);
        }



    }
}

