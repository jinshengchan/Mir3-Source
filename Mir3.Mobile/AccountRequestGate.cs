using System;

namespace Mir3.Mobile
{
    public static class AccountRequestGate
    {
        public static bool TrySend(bool wrongVersion, bool connected, bool loaded, Action send, Action<string> notify)
        {
            if (wrongVersion) { notify("客户端版本或数据库校验失败，请使用服务器匹配的客户端。"); return false; }
            if (!connected) { notify("游戏服务器尚未连接，请查看连接状态后重试。"); return false; }
            if (!loaded) { notify("正在加载服务器信息，请稍后重试。"); return false; }
            send();
            return true;
        }
    }
}
