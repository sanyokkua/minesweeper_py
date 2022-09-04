"""Module contains QDialogForm class."""
import logging

from PyQt6.QtWidgets import (QCheckBox, QComboBox, QFormLayout, QLabel,
                             QSpinBox, QWidget)

from minesweeper_core.constants.configurations import (ADVANCED, BEGINNER,
                                                       INTERMEDIATE)
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
    """Custom Dialog Form widget for new game dialog.

    Args:
        QWidget (_type_): parent widget.
    """

    def __init__(self) -> None:
        """Initialize form with default configuration."""
        QWidget.__init__(self)
        self._number_of_rows: int = BEGINNER.number_of_rows
        self._number_of_columns: int = BEGINNER.number_of_columns
        self._number_of_mines: int = BEGINNER.number_of_mines

        self._configure_widget_layout()
        self._create_widgets()
        self._set_text_to_widgets()
        self._configure_widgets()
        self._add_widgets_to_layout()

    def _configure_widget_layout(self) -> None:
        """Create and configure main widget layout."""
        widget_layout: QFormLayout = QFormLayout(self)
        widget_layout.setContentsMargins(0, 0, 0, 0)
        widget_layout.setSpacing(0)
        self.setLayout(widget_layout)

    def _create_widgets(self) -> None:
        """Create form child widgets."""
        self._label_complexity: QLabel = QLabel(self)
        self._combo_box_complexity: QComboBox = QComboBox(self)
        self._label_number_of_rows: QLabel = QLabel(self)
        self._spin_box_number_of_rows: QSpinBox = QSpinBox(self)
        self._label_number_of_columns: QLabel = QLabel(self)
        self._spin_box_number_of_columns: QSpinBox = QSpinBox(self)
        self._label_number_of_mines: QLabel = QLabel(self)
        self._spin_box_number_of_mines: QSpinBox = QSpinBox(self)
        self._label_custom_settings: QLabel = QLabel(self)
        self._check_box_custom_settings: QCheckBox = QCheckBox(self)

    def _set_text_to_widgets(self) -> None:
        """Set text to the child widgets."""
        self._label_complexity.setText('Choose complexity')
        self._label_number_of_rows.setText('Number of Rows')
        self._label_number_of_columns.setText('Number of Columns')
        self._label_number_of_mines.setText('Number of Mines')
        self._label_custom_settings.setText('Custom settings')
        self._check_box_custom_settings.setText('Complexity')

    def _configure_widgets(self) -> None:
        """Configure all the child widgets."""
        self._configure_combo_box_complexity()
        self._configure_check_box_custom_settings()
        self._configure_spin_box_number_of_rows()
        self._configure_spin_box_number_of_columns()
        self._configure_spin_box_number_of_mines()

    def _configure_combo_box_complexity(self) -> None:
        """Configure combobox used for complexity choose."""
        self._combo_box_complexity.setEditable(False)
        self._combo_box_complexity.addItems(
            [_COMPLEXITY_BEGINNER, _COMPLEXITY_INTERMEDIATE,
             _COMPLEXITY_ADVANCED])
        self._combo_box_complexity.textActivated.connect(
            self._on_combo_box_complexity_text_activated)
        self._enable_combobox_config_options()

    def _configure_check_box_custom_settings(self) -> None:
        """Configure checkbox (switch) for custom settings."""
        self._check_box_custom_settings.setChecked(False)
        self._check_box_custom_settings.stateChanged.connect(
            self._on_check_box_state_changed)

    def _configure_spin_box_number_of_rows(self) -> None:
        """Configure spin box values for the rows field."""
        self._spin_box_number_of_rows.setMinimum(9)
        self._spin_box_number_of_rows.setMaximum(100)
        self._spin_box_number_of_rows.valueChanged.connect(
            self._on_rows_value_changed)

    def _configure_spin_box_number_of_columns(self) -> None:
        """Configure spin box values for the columns field."""
        self._spin_box_number_of_columns.setMinimum(9)
        self._spin_box_number_of_columns.setMaximum(100)
        self._spin_box_number_of_columns.valueChanged.connect(
            self._on_columns_value_changed)

    def _configure_spin_box_number_of_mines(self) -> None:
        """Configure spin box values for the mines field."""
        self._spin_box_number_of_mines.setMinimum(1)
        self._spin_box_number_of_mines.setMaximum(10)
        self._spin_box_number_of_mines.valueChanged.connect(
            self._on_mines_value_changed)

    def _add_widgets_to_layout(self) -> None:
        """Add all configured widgets to the main layout of the form."""
        item_role_label: QFormLayout.ItemRole = QFormLayout.ItemRole.LabelRole
        item_role_field: QFormLayout.ItemRole = QFormLayout.ItemRole.FieldRole
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
        """Handle event of the changed value of rows.

        Args:
            value (int): new value.
        """
        log.debug('_on_rows_value_changed, value: %d', value)
        self._number_of_rows = value
        self._manage_max_number_of_mines()

    def _on_columns_value_changed(self, value: int) -> None:
        """Handle event of the changed value of columns.

        Args:
            value (int): new value
        """
        log.debug('value: %d', value)
        self._number_of_columns = value
        self._manage_max_number_of_mines()

    def _on_mines_value_changed(self, value: int) -> None:
        """Handle event of the changed value of mines.

        Args:
            value (int): new value
        """
        log.debug('value: %d', value)
        self._number_of_mines = value

    def _on_combo_box_complexity_text_activated(self, value: str) -> None:
        """Handle event of the changed value of complexity combobox.

        Args:
            value (str): new value.
        """
        log.debug('value: %s', value)
        config: Configuration = _COMPLEXITY_MAPPING[value]
        self._number_of_rows = config.number_of_rows
        self._number_of_columns = config.number_of_columns
        self._number_of_mines = config.number_of_mines

    def _manage_max_number_of_mines(self) -> None:
        """Calculate number of mines for custom rows/columns numbers."""
        rows: int = self._number_of_rows
        cols: int = self._number_of_columns
        num_cells: int = rows * cols
        max_num_mines: int = num_cells - 10
        self._spin_box_number_of_mines.setMaximum(max_num_mines)

    def _on_check_box_state_changed(self, value: int) -> None:
        """Handle check box state changed event.

        Args:
            value (int): new value. 0 - disabled, 1 - half, 2 - enabled.
        """
        log.debug('value: %d', value)
        if value == 0:
            self._enable_combobox_config_options()
        else:
            self._disable_combobox_config_options()

    def _enable_combobox_config_options(self) -> None:
        """Enable predefined choose options."""
        self._combo_box_complexity.setEnabled(True)
        self._spin_box_number_of_rows.setEnabled(False)
        self._spin_box_number_of_columns.setEnabled(False)
        self._spin_box_number_of_mines.setEnabled(False)

    def _disable_combobox_config_options(self) -> None:
        """Enable custom options edit mode."""
        self._combo_box_complexity.setEnabled(False)
        self._spin_box_number_of_rows.setEnabled(True)
        self._spin_box_number_of_columns.setEnabled(True)
        self._spin_box_number_of_mines.setEnabled(True)

    @property
    def number_of_rows(self) -> int:
        """Return number of rows.

        Returns:
            int: number of rows.
        """
        return self._number_of_rows

    @property
    def number_of_columns(self) -> int:
        """Return number of columns.

        Returns:
            int: number of columns.
        """
        return self._number_of_columns

    @property
    def number_of_mines(self) -> int:
        """Return number of mines.

        Returns:
            int: number of mines.
        """
        return self._number_of_mines
