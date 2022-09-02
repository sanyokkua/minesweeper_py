import logging

from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtWidgets import QFormLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QSpinBox
from PyQt6.QtWidgets import QWidget

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


class QDialogForm(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self._number_of_rows: int = BEGINNER.number_of_rows
        self._number_of_columns: int = BEGINNER.number_of_columns
        self._number_of_mines: int = BEGINNER.number_of_mines

        self._configure_widget_layout()
        self._create_widgets()
        self._set_text_to_widgets()
        self._configure_widgets()
        self._add_widgets_to_layout()

    def _configure_widget_layout(self):
        widget_layout = QFormLayout(self)
        widget_layout.setContentsMargins(0, 0, 0, 0)
        widget_layout.setSpacing(0)
        self.setLayout(widget_layout)

    def _create_widgets(self):
        self._label_complexity = QLabel(self)
        self._combo_box_complexity = QComboBox(self)
        self._label_number_of_rows = QLabel(self)
        self._spin_box_number_of_rows = QSpinBox(self)
        self._label_number_of_columns = QLabel(self)
        self._spin_box_number_of_columns = QSpinBox(self)
        self._label_number_of_mines = QLabel(self)
        self._spin_box_number_of_mines = QSpinBox(self)
        self._label_custom_settings = QLabel(self)
        self._check_box_custom_settings = QCheckBox(self)

    def _set_text_to_widgets(self):
        self._label_complexity.setText('Choose complexity')
        self._label_number_of_rows.setText('Number of Rows')
        self._label_number_of_columns.setText('Number of Columns')
        self._label_number_of_mines.setText('Number of Mines')
        self._label_custom_settings.setText('Custom settings')
        self._check_box_custom_settings.setText('Complexity')

    def _configure_widgets(self):
        self._configure_combo_box_complexity()
        self._configure_check_box_custom_settings()
        self._configure_spin_box_number_of_rows()
        self._configure_spin_box_number_of_columns()
        self._configure_spin_box_number_of_mines()

    def _configure_combo_box_complexity(self):
        self._combo_box_complexity.setEditable(False)
        self._combo_box_complexity.addItems([_COMPLEXITY_BEGINNER, _COMPLEXITY_INTERMEDIATE, _COMPLEXITY_ADVANCED])
        self._combo_box_complexity.textActivated.connect(self._on_combo_box_complexity_text_activated)
        self._enable_combobox_config_options()

    def _configure_check_box_custom_settings(self):
        self._check_box_custom_settings.setChecked(False)
        self._check_box_custom_settings.stateChanged.connect(self._on_check_box_state_changed)

    def _configure_spin_box_number_of_rows(self):
        self._spin_box_number_of_rows.setMinimum(9)
        self._spin_box_number_of_rows.setMaximum(100)
        self._spin_box_number_of_rows.valueChanged.connect(self._on_rows_value_changed)

    def _configure_spin_box_number_of_columns(self):
        self._spin_box_number_of_columns.setMinimum(9)
        self._spin_box_number_of_columns.setMaximum(100)
        self._spin_box_number_of_columns.valueChanged.connect(self._on_columns_value_changed)

    def _configure_spin_box_number_of_mines(self):
        self._spin_box_number_of_mines.setMinimum(1)
        self._spin_box_number_of_mines.setMaximum(10)
        self._spin_box_number_of_mines.valueChanged.connect(self._on_mines_value_changed)

    def _add_widgets_to_layout(self):
        item_role_label = QFormLayout.ItemRole.LabelRole
        item_role_field = QFormLayout.ItemRole.FieldRole
        layout: QFormLayout = self.layout()
        layout.setWidget(0, item_role_label, self._label_complexity)
        layout.setWidget(0, item_role_field, self._combo_box_complexity)
        layout.setWidget(1, item_role_label, self._label_custom_settings)
        layout.setWidget(1, item_role_field, self._check_box_custom_settings)
        layout.setWidget(2, item_role_label, self._label_number_of_rows)
        layout.setWidget(2, item_role_field, self._spin_box_number_of_rows)
        layout.setWidget(3, item_role_label, self._label_number_of_columns)
        layout.setWidget(3, item_role_field, self._spin_box_number_of_columns)
        layout.setWidget(4, item_role_label, self._label_number_of_mines)
        layout.setWidget(4, item_role_field, self._spin_box_number_of_mines)

    def _on_rows_value_changed(self, value: int) -> None:
        log.debug('_on_rows_value_changed, value: %d', value)
        self._number_of_rows = value
        self._manage_max_number_of_mines()

    def _on_columns_value_changed(self, value: int) -> None:
        log.debug('value: %d', value)
        self._number_of_columns = value
        self._manage_max_number_of_mines()

    def _on_mines_value_changed(self, value: int) -> None:
        log.debug('value: %d', value)
        self._number_of_mines = value

    def _on_combo_box_complexity_text_activated(self, value: str) -> None:
        log.debug('value: %s', value)
        config = _COMPLEXITY_MAPPING[value]
        self._number_of_rows = config.number_of_rows
        self._number_of_columns = config.number_of_columns
        self._number_of_mines = config.number_of_mines

    def _manage_max_number_of_mines(self) -> None:
        rows = self._number_of_rows
        cols = self._number_of_columns
        num_cells = rows * cols
        max_num_mines = num_cells - 10
        self._spin_box_number_of_mines.setMaximum(max_num_mines)

    def _on_check_box_state_changed(self, value: int) -> None:
        log.debug('value: %d', value)
        if value == 0:
            self._enable_combobox_config_options()
        else:
            self._disable_combobox_config_options()

    def _enable_combobox_config_options(self) -> None:
        self._combo_box_complexity.setEnabled(True)
        self._spin_box_number_of_rows.setEnabled(False)
        self._spin_box_number_of_columns.setEnabled(False)
        self._spin_box_number_of_mines.setEnabled(False)

    def _disable_combobox_config_options(self) -> None:
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
