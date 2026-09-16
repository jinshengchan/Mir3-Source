using DevExpress.XtraEditors;
using DevExpress.XtraGrid.Views.Grid;
using Server.Envir;
using System;
using MirDB;
using System.Windows.Forms;
using Server.DBModels;
using System.Drawing;
using System.ComponentModel;
using System.Text;
using System.Security.Cryptography;

namespace Server.Views
{
    public partial class AccountView : DevExpress.XtraEditors.XtraForm
    {
        public AccountView()
        {
            InitializeComponent();
            InitializeDataBinding();
            SetupPasswordColumn();
            SetupEventHandlers();
        }

        private void SetupEventHandlers()
        {
            this.AccountGridView.MouseDown += AccountGridView_MouseDown;
            this.AccountGridView.DoubleClick += AccountGridView_DoubleClick;
            this.AccountGridView.CustomDrawCell += AccountGridView_CustomDrawCell;
        }

        private void InitializeDataBinding()
        {
            try
            {
                SMain.SetUpView(AccountGridView);

                if (SEnvir.AccountInfoList != null)
                {
                    AccountGridControl.DataSource = SEnvir.AccountInfoList.Binding;
                    if (AccountLookUpEdit != null)
                    {
                        AccountLookUpEdit.DataSource = SEnvir.AccountInfoList.Binding;
                    }
                }

                AccountGridView.OptionsSelection.MultiSelect = true;
                AccountGridView.OptionsSelection.MultiSelectMode = GridMultiSelectMode.CellSelect;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"初始化数据绑定失败: {ex.Message}");
            }
        }

        private void SetupPasswordColumn()
        {
            if (gridColumn20 != null)
            {
                gridColumn20.OptionsColumn.AllowEdit = false;
            }
        }

        // 事件处理方法
        private void AccountGridView_MouseDown(object sender, MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Right)
            {
                var hitInfo = AccountGridView.CalcHitInfo(e.Location);
                if (hitInfo.InRow)
                {
                    AccountGridView.FocusedRowHandle = hitInfo.RowHandle;
                    ShowContextMenu(e.Location);
                }
            }
        }

        private void AccountGridView_DoubleClick(object sender, EventArgs e)
        {
            var hitInfo = AccountGridView.CalcHitInfo(AccountGridControl.PointToClient(Cursor.Position));
            if (hitInfo.InRowCell && hitInfo.Column == gridColumn20)
            {
                var account = AccountGridView.GetRow(hitInfo.RowHandle) as AccountInfo;
                if (account != null)
                {
                    string passwordInfo = GetPasswordInfo(account);
                    XtraMessageBox.Show(passwordInfo, "密码信息", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
        }

        private void AccountGridView_CustomDrawCell(object sender, DevExpress.XtraGrid.Views.Base.RowCellCustomDrawEventArgs e)
        {
            if (e.Column == gridColumn20)
            {
                e.DisplayText = "******";
                e.Appearance.ForeColor = Color.Gray;
            }
        }

        private void ShowContextMenu(Point location)
        {
            try
            {
                ContextMenuStrip contextMenu = new ContextMenuStrip();

                ToolStripMenuItem showPasswordItem = new ToolStripMenuItem("显示密码信息");
                showPasswordItem.Click += ShowPasswordInfo_Click;

                ToolStripMenuItem resetPasswordItem = new ToolStripMenuItem("重置密码");
                resetPasswordItem.Click += ResetPassword_Click;

                ToolStripMenuItem debugPasswordItem = new ToolStripMenuItem("调试密码信息");
                debugPasswordItem.Click += DebugPasswordItem_Click;

                contextMenu.Items.Add(showPasswordItem);
                contextMenu.Items.Add(resetPasswordItem);
                contextMenu.Items.Add(new ToolStripSeparator());
                contextMenu.Items.Add(debugPasswordItem);

                contextMenu.Show(AccountGridControl, location);
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"显示右键菜单失败: {ex.Message}");
            }
        }

        private void ShowPasswordInfo_Click(object sender, EventArgs e)
        {
            try
            {
                var account = AccountGridView.GetFocusedRow() as AccountInfo;
                if (account != null)
                {
                    string accountName = GetAccountName(account);
                    string passwordInfo = GetPasswordInfo(account);

                    XtraMessageBox.Show($"账号: {accountName}\n{passwordInfo}",
                        "密码信息", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else
                {
                    XtraMessageBox.Show("请选择一个有效的账号！", "提示", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                }
            }
            catch (Exception ex)
            {
                XtraMessageBox.Show($"显示密码信息失败: {ex.Message}", "错误", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void ResetPassword_Click(object sender, EventArgs e)
        {
            try
            {
                var account = AccountGridView.GetFocusedRow() as AccountInfo;
                if (account != null)
                {
                    string accountName = GetAccountName(account);

                    if (XtraMessageBox.Show($"确定要重置账号 {accountName} 的密码为 123456 吗？",
                        "确认重置", MessageBoxButtons.YesNo, MessageBoxIcon.Question) == DialogResult.Yes)
                    {
                        bool success = SetPassword(account, "123456");
                        if (success)
                        {
                            RefreshData();
                            XtraMessageBox.Show("密码重置成功！", "提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        }
                        else
                        {
                            XtraMessageBox.Show("密码重置失败！", "错误", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        }
                    }
                }
                else
                {
                    XtraMessageBox.Show("请选择一个有效的账号！", "提示", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                }
            }
            catch (Exception ex)
            {
                XtraMessageBox.Show($"重置密码失败: {ex.Message}", "错误", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void DebugPasswordItem_Click(object sender, EventArgs e)
        {
            try
            {
                var account = AccountGridView.GetFocusedRow() as AccountInfo;
                if (account != null)
                {
                    DebugPasswordInfo(account);
                }
            }
            catch (Exception ex)
            {
                XtraMessageBox.Show($"调试失败: {ex.Message}", "错误", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        // 刷新数据
        private void RefreshData()
        {
            try
            {
                if (SEnvir.AccountInfoList != null)
                {
                    var bindingList = SEnvir.AccountInfoList.Binding as BindingList<AccountInfo>;
                    bindingList?.ResetBindings();
                }
                AccountGridView.BestFitColumns();
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"刷新数据失败: {ex.Message}");
            }
        }

        private string GetAccountName(AccountInfo account)
        {
            try
            {
                return account.EMailAddress ?? "未知账号";
            }
            catch
            {
                return "未知账号";
            }
        }

        // 获取密码信息 - 由于密码是加密的，无法直接显示明文
        private string GetPasswordInfo(AccountInfo account)
        {
            try
            {
                var passwordProperty = typeof(AccountInfo).GetProperty("Password");
                if (passwordProperty != null)
                {
                    var passwordValue = passwordProperty.GetValue(account);

                    if (passwordValue is byte[] passwordBytes)
                    {
                        return GetPasswordHashInfo(passwordBytes);
                    }

                    return $"密码类型: {passwordValue?.GetType().Name ?? "null"}\n密码值: {passwordValue}";
                }
                return "无密码信息";
            }
            catch (Exception ex)
            {
                return $"获取密码信息失败: {ex.Message}";
            }
        }

        // 获取密码哈希的详细信息
        private string GetPasswordHashInfo(byte[] totalHash)
        {
            if (totalHash == null || totalHash.Length == 0)
                return "密码为空";

            StringBuilder info = new StringBuilder();
            info.AppendLine("=== 密码信息 ===");
            info.AppendLine($"加密方式: PBKDF2 (Rfc2898DeriveBytes)");
            info.AppendLine($"哈希长度: {totalHash.Length} 字节");

            if (totalHash.Length >= 36) // SaltSize(16) + hashSize(20) = 36
            {
                byte[] salt = new byte[16];
                byte[] hash = new byte[20];

                Buffer.BlockCopy(totalHash, 0, salt, 0, 16);
                Buffer.BlockCopy(totalHash, 16, hash, 0, 20);

                info.AppendLine($"盐(Salt): {BitConverter.ToString(salt).Replace("-", "")}");
                info.AppendLine($"哈希值: {BitConverter.ToString(hash).Replace("-", "")}");
                info.AppendLine($"迭代次数: 1354");

                // 测试常见密码
                info.AppendLine($"\n=== 密码测试 ===");
                string[] commonPasswords = { "123456", "password", "12345678", "qwerty", "abc123", "111111", "admin" };
                bool found = false;

                foreach (string testPassword in commonPasswords)
                {
                    if (PasswordMatch(testPassword, totalHash))
                    {
                        info.AppendLine($"匹配密码: {testPassword}");
                        found = true;
                        break;
                    }
                }

                if (!found)
                {
                    info.AppendLine("未匹配到常见密码");
                    info.AppendLine("提示: 密码已安全加密，无法直接显示明文");
                }
            }
            else
            {
                info.AppendLine($"哈希数据: {BitConverter.ToString(totalHash).Replace("-", "")}");
                info.AppendLine("警告: 密码格式异常");
            }

            return info.ToString();
        }

        #region Password Encryption Methods

        /// <summary>
        /// 迭代次数
        /// </summary>
        private const int Iterations = 1354;
        /// <summary>
        /// 盐粒子大小
        /// </summary>
        private const int SaltSize = 16;
        /// <summary>
        /// 哈希值大小
        /// </summary>
        private const int hashSize = 20;

        /// <summary>
        /// 创建加密密匙
        /// </summary>
        private static byte[] CreateHash(string password)
        {
            using (RNGCryptoServiceProvider rng = new RNGCryptoServiceProvider())
            {
                byte[] salt = new byte[SaltSize];
                rng.GetBytes(salt);

                using (Rfc2898DeriveBytes rfc = new Rfc2898DeriveBytes(password, salt, Iterations))
                {
                    byte[] hash = rfc.GetBytes(hashSize);

                    byte[] totalHash = new byte[SaltSize + hashSize];
                    Buffer.BlockCopy(salt, 0, totalHash, 0, SaltSize);
                    Buffer.BlockCopy(hash, 0, totalHash, SaltSize, hashSize);

                    return totalHash;
                }
            }
        }

        /// <summary>
        /// 密码匹配
        /// </summary>
        private static bool PasswordMatch(string password, byte[] totalHash)
        {
            try
            {
                if (totalHash.Length != SaltSize + hashSize)
                    return false;

                byte[] salt = new byte[SaltSize];
                Buffer.BlockCopy(totalHash, 0, salt, 0, SaltSize);

                using (Rfc2898DeriveBytes rfc = new Rfc2898DeriveBytes(password, salt, Iterations))
                {
                    byte[] hash = rfc.GetBytes(hashSize);

                    // 比较哈希值
                    for (int i = 0; i < hashSize; i++)
                    {
                        if (totalHash[SaltSize + i] != hash[i])
                            return false;
                    }
                    return true;
                }
            }
            catch
            {
                return false;
            }
        }

        #endregion

        // 设置密码 - 使用相同的加密方式
        private bool SetPassword(AccountInfo account, string newPassword)
        {
            try
            {
                var passwordProperty = typeof(AccountInfo).GetProperty("Password");
                if (passwordProperty != null)
                {
                    var propertyType = passwordProperty.PropertyType;

                    if (propertyType == typeof(byte[]))
                    {
                        // 使用PBKDF2加密新密码
                        byte[] encryptedPassword = CreateHash(newPassword);
                        passwordProperty.SetValue(account, encryptedPassword);
                    }
                    else if (propertyType == typeof(string))
                    {
                        passwordProperty.SetValue(account, newPassword);
                    }

                    SaveAccountChanges();
                    return true;
                }
                return false;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"设置密码失败: {ex.Message}");
                return false;
            }
        }

        // 保存账号更改
        private void SaveAccountChanges()
        {
            try
            {
                if (SMain.Session != null)
                {
                    var saveMethod = SMain.Session.GetType().GetMethod("Save", new Type[] { typeof(bool) });
                    saveMethod?.Invoke(SMain.Session, new object[] { false });
                }
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"保存更改失败: {ex.Message}");
            }
        }

        // 调试密码信息
        private void DebugPasswordInfo(AccountInfo account)
        {
            try
            {
                var passwordProperty = typeof(AccountInfo).GetProperty("Password");
                if (passwordProperty != null)
                {
                    var passwordValue = passwordProperty.GetValue(account);

                    StringBuilder debugInfo = new StringBuilder();
                    debugInfo.AppendLine("=== 密码调试信息 ===");

                    if (passwordValue is byte[] passwordBytes)
                    {
                        debugInfo.AppendLine($"密码类型: byte[] (PBKDF2加密)");
                        debugInfo.AppendLine($"字节长度: {passwordBytes.Length}");
                        debugInfo.AppendLine($"十六进制: {BitConverter.ToString(passwordBytes)}");
                        debugInfo.AppendLine($"Base64: {Convert.ToBase64String(passwordBytes)}");

                        if (passwordBytes.Length >= 36)
                        {
                            byte[] salt = new byte[16];
                            byte[] hash = new byte[20];
                            Buffer.BlockCopy(passwordBytes, 0, salt, 0, 16);
                            Buffer.BlockCopy(passwordBytes, 16, hash, 0, 20);

                            debugInfo.AppendLine($"盐(Salt): {BitConverter.ToString(salt)}");
                            debugInfo.AppendLine($"哈希值: {BitConverter.ToString(hash)}");
                        }
                    }
                    else
                    {
                        debugInfo.AppendLine($"密码类型: {passwordValue?.GetType().Name ?? "null"}");
                        debugInfo.AppendLine($"密码值: {passwordValue}");
                    }

                    XtraMessageBox.Show(debugInfo.ToString(), "密码调试信息",
                        MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
            catch (Exception ex)
            {
                XtraMessageBox.Show($"调试失败: {ex.Message}", "错误", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        // 窗体加载完成
        protected override void OnShown(EventArgs e)
        {
            base.OnShown(e);
            try
            {
                AccountGridView.BestFitColumns();
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"窗体显示初始化失败: {ex.Message}");
            }
        }
    }
}