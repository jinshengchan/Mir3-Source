using DevExpress.XtraEditors;
using DevExpress.XtraGrid;
using DevExpress.XtraGrid.Columns;
using DevExpress.XtraGrid.Views.Grid;
using Server.Envir;

namespace Server.Views
{
    public partial class CharacterView : XtraForm
    {
        public CharacterView()        //角色视图
        {
            InitializeComponent();

            CharacterGridControl.ViewRegistered += CharacterGridControl_ViewRegistered;
            CharacterGridControl.DataSource = SEnvir.CharacterInfoList?.Binding;
            AccountLookUpEdit.DataSource = SEnvir.AccountInfoList?.Binding;

            CharacterGridView.OptionsSelection.MultiSelect = true;
            CharacterGridView.OptionsSelection.MultiSelectMode = DevExpress.XtraGrid.Views.Grid.GridMultiSelectMode.CellSelect;
        }

        private void CharacterGridControl_ViewRegistered(object sender, ViewOperationEventArgs e)
        {
            GridView view = e.View as GridView;
            if (view == null || view.LevelName != "Magics") return;

            EnsureMagicNameColumn(view);
            SMain.SetUpView(view);
        }

        private static void EnsureMagicNameColumn(GridView view)
        {
            GridColumn nameColumn = view.Columns.ColumnByFieldName("Info.Name");
            if (nameColumn == null)
            {
                nameColumn = view.Columns.AddField("Info.Name");
                nameColumn.Visible = true;
            }

            nameColumn.Caption = "技能名称";
            nameColumn.OptionsColumn.AllowEdit = false;

            GridColumn infoColumn = view.Columns.ColumnByFieldName("Info");
            if (infoColumn != null && infoColumn.Visible)
                nameColumn.VisibleIndex = infoColumn.VisibleIndex + 1;
        }
    }
}
