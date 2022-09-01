import logging

from PyQt6.QtCore import QRect
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QDialogButtonBox
from PyQt6.QtWidgets import QFormLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QSpinBox
from PyQt6.QtWidgets import QVBoxLayout

from minesweeper_core.constants.default_configurations import ADVANCED
from minesweeper_core.constants.default_configurations import BEGINNER
from minesweeper_core.constants.default_configurations import INTERMEDIATE
from minesweeper_core.data.field_configuration import Configuration

log: logging.Logger = logging.getLogger(__name__)

_COMPLEXITY_BEGINNER: str = 'BEGINNER'
_COMPLEXITY_INTERMEDIATE: str = 'INTERMEDIATE'
_COMPLEXITY_ADVANCED: str = 'ADVANCED'

_COMPLEXITY_MAPPING: dict[str, Configuration] = {
    _COMPLEXITY_BEGINNER: BEGINNER,
    _COMPLEXITY_INTERMEDIATE: INTERMEDIATE,
    _COMPLEXITY_ADVANCED: ADVANCED
}


class QtWidgetNewGamePopup(QDialog):
    def __init__(self) -> None:
        log.debug('__init__ of NewGame PopUp')
        QDialog.__init__(self)
        self.setWindowTitle('Dialog')
        self._create_window_layout()
        self._create_dialog_main_layout()
        self._create_dialog_form_layout()
        self._create_control_widget_labels()
        self._create_control_widgets()
        self._set_widgets_text()
        self._create_dialog_buttons()
        self._compose_control_widgets_form()
        self._compose_dialog_main_layout()
        self._configure_spin_box_defaults()
        self._configure_combo_box_defaults()
        self._configure_check_box_defaults()
        self._add_spin_box_signal_handlers()
        self._add_combo_box_signal_handlers()
        self._add_check_box_signal_handlers()
        self._number_of_rows: int = BEGINNER.number_of_rows
        self._number_of_columns: int = BEGINNER.number_of_columns
        self._number_of_mines: int = BEGINNER.number_of_mines
        log.debug('__init__ of NewGame PopUp end')

    def _create_window_layout(self) -> None:
        log.debug('_create_window_layout')
        self._verticalLayoutWidget = QVBoxLayout()
        size = QSize(380, 190)
        minimum_size = QRect(0, 0, 380, 190)
        self._verticalLayoutWidget.setGeometry(minimum_size)
        self.setFixedSize(size)

    def _create_dialog_main_layout(self) -> None:
        log.debug('_create_dialog_main_layout')
        self._dialog_main_vertical_layout = QVBoxLayout(self._verticalLayoutWidget)
        self._dialog_main_vertical_layout.setContentsMargins(0, 0, 0, 0)
        self._dialog_main_vertical_layout.setSpacing(0)

    def _create_dialog_form_layout(self) -> None:
        log.debug('_create_dialog_form_layout')
        self._dialog_form_layout = QFormLayout()
        self._dialog_form_layout.setSpacing(0)

    def _create_control_widget_labels(self) -> None:
        log.debug('_create_control_widget_labels')
        self._label_complexity = QLabel(self._dialog_form_layout)
        self._label_number_of_rows = QLabel(self._dialog_form_layout)
        self._label_number_of_columns = QLabel(self._dialog_form_layout)
        self._label_number_of_mines = QLabel(self._dialog_form_layout)
        self._label_custom_settings = QLabel(self._dialog_form_layout)

    def _create_control_widgets(self) -> None:
        log.debug('_create_control_widgets')
        self._combo_box_complexity = QComboBox(self._dialog_form_layout)
        self._check_box_custom_settings = QCheckBox(self._dialog_form_layout)
        self._spin_box_number_of_rows = QSpinBox(self._dialog_form_layout)
        self._spin_box_number_of_columns = QSpinBox(self._dialog_form_layout)
        self._spin_box_number_of_mines = QSpinBox(self._dialog_form_layout)

    def _set_widgets_text(self) -> None:
        log.debug('_set_widgets_text')
        self._label_complexity.setText('Choose complexity')
        self._check_box_custom_settings.setText('Complexity')
        self._label_number_of_rows.setText('Number of Rows')
        self._label_number_of_columns.setText('Number of Columns')
        self._label_number_of_mines.setText('Number of Mines')
        self._label_custom_settings.setText('Custom settings')

    def _create_dialog_buttons(self) -> None:
        log.debug('_create_dialog_buttons')
        self._dialog_button_box = QDialogButtonBox(self._dialog_form_layout)
        self._dialog_button_box.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        self._dialog_button_box.accepted.connect(self.accept)
        self._dialog_button_box.rejected.connect(self.reject)

    def _compose_control_widgets_form(self) -> None:
        log.debug('_compose_control_widgets_form')
        label_role = QFormLayout.ItemRole.LabelRole
        field_role = QFormLayout.ItemRole.FieldRole
        self._dialog_form_layout.setWidget(0, label_role, self._label_complexity)
        self._dialog_form_layout.setWidget(0, field_role, self._combo_box_complexity)
        self._dialog_form_layout.setWidget(1, label_role, self._label_custom_settings)
        self._dialog_form_layout.setWidget(1, field_role, self._check_box_custom_settings)
        self._dialog_form_layout.setWidget(2, label_role, self._label_number_of_rows)
        self._dialog_form_layout.setWidget(2, field_role, self._spin_box_number_of_rows)
        self._dialog_form_layout.setWidget(3, label_role, self._label_number_of_columns)
        self._dialog_form_layout.setWidget(3, field_role, self._spin_box_number_of_columns)
        self._dialog_form_layout.setWidget(4, label_role, self._label_number_of_mines)
        self._dialog_form_layout.setWidget(4, field_role, self._spin_box_number_of_mines)

    def _compose_dialog_main_layout(self) -> None:
        log.debug('_compose_dialog_main_layout')
        self._dialog_main_vertical_layout.addLayout(self._dialog_form_layout)
        self._dialog_main_vertical_layout.addWidget(self._dialog_button_box)
        self._verticalLayoutWidget.addLayout(self._dialog_main_vertical_layout)

    def _configure_combo_box_defaults(self) -> None:
        log.debug('_configure_combo_box_defaults')
        self._combo_box_complexity.setEditable(False)
        self._combo_box_complexity.addItems([_COMPLEXITY_BEGINNER, _COMPLEXITY_INTERMEDIATE, _COMPLEXITY_ADVANCED])
        self._enable_combobox_config_options()

    def _configure_spin_box_defaults(self) -> None:
        log.debug('_configure_spin_box_defaults')
        self._spin_box_number_of_rows.setMinimum(9)
        self._spin_box_number_of_rows.setMaximum(100)
        self._spin_box_number_of_columns.setMinimum(9)
        self._spin_box_number_of_columns.setMaximum(100)
        self._spin_box_number_of_mines.setMinimum(1)
        self._spin_box_number_of_mines.setMaximum(10)

    def _configure_check_box_defaults(self) -> None:
        log.debug('_configure_check_box_defaults')
        self._check_box_custom_settings.setChecked(False)

    def _add_spin_box_signal_handlers(self) -> None:
        log.debug('_add_spin_box_signal_handlers')
        self._spin_box_number_of_rows.valueChanged.connect(self._on_rows_value_changed)
        self._spin_box_number_of_columns.valueChanged.connect(self._on_columns_value_changed)
        self._spin_box_number_of_mines.valueChanged.connect(self._on_mines_value_changed)

    def _add_combo_box_signal_handlers(self) -> None:
        log.debug('_add_combo_box_signal_handlers')
        self._combo_box_complexity.textActivated.connect(self._on_combo_box_complexity_text_activated)

    def _add_check_box_signal_handlers(self) -> None:
        log.debug('_add_check_box_signal_handlers')
        self._check_box_custom_settings.stateChanged.connect(self._on_check_box_state_changed)

    def _on_rows_value_changed(self, value: int) -> None:
        log.debug('_on_rows_value_changed, value: %d', value)
        self._number_of_rows = value
        self._manage_max_number_of_mines()

    def _on_columns_value_changed(self, value: int) -> None:
        log.debug('_on_columns_value_changed, value: %d', value)
        self._number_of_columns = value
        self._manage_max_number_of_mines()

    def _on_mines_value_changed(self, value: int) -> None:
        log.debug('_on_mines_value_changed, value: %d', value)
        self._number_of_mines = value

    def _on_combo_box_complexity_text_activated(self, value: str) -> None:
        log.debug('_on_combo_box_complexity_text_activated, value: %s', value)
        config = _COMPLEXITY_MAPPING[value]
        self._number_of_rows = config.number_of_rows
        self._number_of_columns = config.number_of_columns
        self._number_of_mines = config.number_of_mines

    def _manage_max_number_of_mines(self) -> None:
        log.debug('_manage_max_number_of_mines')
        rows = self.number_of_rows
        cols = self.number_of_columns
        num_cells = rows * cols
        max_num_mines = num_cells - 10
        self._spin_box_number_of_mines.setMaximum(max_num_mines)

    def _on_check_box_state_changed(self, value: int) -> None:
        log.debug('_on_check_box_state_changed, value: %d', value)
        # https://doc.qt.io/qt-6/qt.html#CheckState-enum
        if value == 0:
            self._enable_combobox_config_options()
        else:
            self._disable_combobox_config_options()

    def _enable_combobox_config_options(self) -> None:
        log.debug('_enable_combobox_config_options')
        self._combo_box_complexity.setEnabled(True)
        self._spin_box_number_of_rows.setEnabled(False)
        self._spin_box_number_of_columns.setEnabled(False)
        self._spin_box_number_of_mines.setEnabled(False)

    def _disable_combobox_config_options(self) -> None:
        log.debug('_disable_combobox_config_options')
        self._combo_box_complexity.setEnabled(False)
        self._spin_box_number_of_rows.setEnabled(True)
        self._spin_box_number_of_columns.setEnabled(True)
        self._spin_box_number_of_mines.setEnabled(True)

    @property
    def number_of_rows(self) -> int:
        return self._number_of_rows

    @property
    def number_of_columns(self) -> int:
        return self._number_of_columns

    @property
    def number_of_mines(self) -> int:
        return self._number_of_mines
