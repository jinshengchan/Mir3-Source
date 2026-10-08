#if ANDROID && BUNDLED_RESOURCE_TEST && !REPOSITORY_SERVER_PROTOCOL
using System.Collections.Generic;
using System.Drawing;

// The working 1403 APK includes these five packet types. Packet IDs are assigned
// by sorting all Packet subclasses, so omitting even an unused type shifts IDs.
// Keep the original names and serialized property order for that test server.
namespace Library.Network.ClientPackets
{
    public sealed class CompanionItemsToInventory : Packet { }

    public sealed class TeamHookLeaderLocation : Packet
    {
        public string LeaderName { get; set; }
    }

    public sealed class TeamHookTownSupply : Packet
    {
        public List<int> StoreSlots { get; set; }
        public List<int> SellInventorySlots { get; set; }
        public List<int> SellCompanionSlots { get; set; }
        public List<int> ItemIndexes { get; set; }
        public List<int> TargetCounts { get; set; }
    }
}

namespace Library.Network.ServerPackets
{
    public sealed class TeamHookLeaderLocation : Packet
    {
        public bool Valid { get; set; }
        public int MapIndex { get; set; }
        public Point Location { get; set; }
    }

    public sealed class TeamHookTownSupply : Packet
    {
        public bool Complete { get; set; }
    }
}
#endif
