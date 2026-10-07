using Android.Views;
using Android.Widget;
using Client.Envir;
using System;
using C = Library.Network.ClientPackets;

namespace Mir3.Droid
{
    public partial class MainActivity
    {
        #region 属性
        string _account = "", _password = "";
        public string Account
        {
            get => _account;
            set
            {
                _account = value ?? "";
                Config.RememberedEMail = _account;
                BeginInvoke(() =>
                {
                    var input = _overLayout?.FindViewById<EditText>(Resource.Id.acc);
                    if (input != null) input.Text = _account;
                });
            }
        }

        public string Pwd
        {
            get => _password;
            set
            {
                _password = value ?? "";
                Config.RememberedPassword = _password;
                BeginInvoke(() =>
                {
                    var input = _overLayout?.FindViewById<EditText>(Resource.Id.pwd);
                    if (input != null) input.Text = _password;
                });
            }
        }
        #endregion

        public void InitLogin() => BeginInvoke(InitializeLoginView);

        string _loginStatus = "正在连接游戏服务器...";
        public void SetLoginStatus(string status)
        {
            _loginStatus = status;
            BeginInvoke(() =>
            {
                var label = _overLayout?.FindViewById<TextView>(Resource.Id.login_status);
                if (label != null) label.Text = status;
            });
        }

        bool SubmitAccountRequest(Library.Network.Packet packet)
        {
            var connection = CEnvir.Connection;
            try
            {
                bool sent = Mir3.Mobile.AccountRequestGate.TrySend(CEnvir.WrongVersion,
                    connection != null && connection.ServerConnected && !connection.Disconnecting,
                    CEnvir.Loaded, () => connection.Enqueue(packet), ShowMsg);
                if (sent) ShowMsg("请求已提交，请等待服务器回复。");
                return sent;
            }
            catch (Exception ex)
            {
                CEnvir.SaveError(ex.ToString());
                ShowMsg("请求发送失败，请检查连接状态。");
                return false;
            }
        }

        private void InitializeLoginView()
        {
            var view = View.Inflate(this, Resource.Layout.login, null);
            var newBtn = view.FindViewById<ImageButton>(Resource.Id.newAcount);
            newBtn.Click -= NewBtn_Click;
            newBtn.Click += NewBtn_Click;

            var change = view.FindViewById<ImageButton>(Resource.Id.changePwd);
            change.Click -= Change_Click;
            change.Click += Change_Click;

            var forget = view.FindViewById<ImageButton>(Resource.Id.forgetPwd);
            forget.Click -= Forget_Click;
            forget.Click += Forget_Click;

            var exit = view.FindViewById<ImageButton>(Resource.Id.exit);
            exit.Click -= Exit_Click;
            exit.Click += Exit_Click;


            var loginBtn = view.FindViewById<ImageButton>(Resource.Id.login_btn);
            loginBtn.Click -= LoginBtn_Click;
            loginBtn.Click += LoginBtn_Click;
            view.FindViewById<EditText>(Resource.Id.acc).TextChanged += (sender, args) => _account = ((EditText)sender).Text ?? "";
            view.FindViewById<EditText>(Resource.Id.pwd).TextChanged += (sender, args) => _password = ((EditText)sender).Text ?? "";
            AddView(view);

            Account = Config.RememberedEMail;
            Pwd = Config.RememberedPassword;
            SetLoginStatus(_loginStatus);
        }

        private void Forget_Click(object sender, EventArgs e)
        {
            #region action sheet
            var sheet = new BottomActionSheet(this);
            var view = View.Inflate(this, Resource.Layout.sheet_forget, null);
            var email = view.FindViewById<LinearLayout>(Resource.Id.get_code);
            var useCode = view.FindViewById<LinearLayout>(Resource.Id.use_code);
            var cancel = view.FindViewById<LinearLayout>(Resource.Id.cancel);
            email.Touch += (s, e) =>
            {
                sheet.Dismiss();
                ShowForgetPwd(true);
            };
            useCode.Touch += (s, e) =>
            {
                sheet.Dismiss();
                ShowForgetPwd(false);
            };
            cancel.Touch += (s, e) =>
            {
                sheet.Dismiss();
            };
            sheet.SetContentView(view);
            sheet.Show();
            #endregion

            #region 普通窗口
            //_currentWindow = GetWindow(Resource.Layout.sheet_forget);
            //var view = _currentWindow.ContentView;
            //var email = view.FindViewById<LinearLayout>(Resource.Id.get_code);
            //var useCode = view.FindViewById<LinearLayout>(Resource.Id.use_code);
            //var cancel = view.FindViewById<LinearLayout>(Resource.Id.cancel);
            //email.Touch += (s, e) =>
            //{
            //    _currentWindow?.Dismiss();
            //    ShowForgetPwd(true);
            //};
            //useCode.Touch += (s, e) =>
            //{
            //    _currentWindow?.Dismiss();
            //    ShowForgetPwd(false);
            //};
            //cancel.Touch += (s, e) =>
            //{
            //    _currentWindow?.Dismiss();
            //};
            //_currentWindow.ShowAtLocation(_overLayout, GravityFlags.CenterVertical, 0, 0);
            #endregion
        }
        private void Exit_Click(object sender, EventArgs e)
        {
            Exit();
        }

        private void Change_Click(object sender, EventArgs e)
        {
            ShowChangePwd();
        }

        private void LoginBtn_Click(object sender, EventArgs e)
        {
#if !DEBUG
            if (Helpers.VerifyDevice.Verify())
            {
               // ShowMsg("禁止模拟器中登录游戏!");
              //  return;
            }
#endif
            if (string.IsNullOrWhiteSpace(Account) || string.IsNullOrEmpty(Pwd))
            {
                ShowMsg("请输入账号和密码。");
                return;
            }
            C.Login packet = new C.Login
            {
                EMailAddress = Account,
                Password = Pwd,
                CheckSum = CEnvir.C,
            };

            SubmitAccountRequest(packet);
        }

        private void NewBtn_Click(object sender, EventArgs e)
        {
            ShowCreat();
        }
    }
}

