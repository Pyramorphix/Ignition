import numpy as np
from PIL import Image
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGroupBox, QRadioButton, QComboBox, 
                             QLabel, QPushButton, QColorDialog, QSlider, 
                             QFormLayout, QFileDialog, QCheckBox)
from PyQt6.QtGui import QPixmap, QImage, QColor
from PyQt6.QtCore import Qt, QTimer

from preset_manager import load_presets


class App(QMainWindow):
# ╭──────────────────────────────────────────────────────────╮
# │                   Class initialization                   │
# ╰──────────────────────────────────────────────────────────╯
    def __init__(self):
    # ╭─ Init ─────────────╮
        super().__init__()
    # ╰────────────────────╯

    # ╭─ Window ────────────────────────╮
        self.setWindowTitle("Ignition")
        self.setMinimumSize(800, 500)
    # ╰─────────────────────────────────╯

    # ╭─ State ─────────────────────────╮
        self.current_preset = None
        self.current_params = {}
        self.current_image_array = None
        self.anim_frame = 0
    # ╰─────────────────────────────────╯

    # ╭─ Loading presets ─────────────╮
        self.presets = load_presets()
    # ╰───────────────────────────────╯

    # ╭─ Putting up UI ───────────╮
        self.init_ui()
        self.update_preset_list()
    # ╰───────────────────────────╯


# ╭──────────────────────────────────────────────────────────╮
# │                         UI setup                         │
# ╰──────────────────────────────────────────────────────────╯
    def init_ui(self):
    # ╭─ Main widget layout ───────────────────╮
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
    # ╰────────────────────────────────────────╯

    # ╭─ Left panel: select and configure presets ─────────────────────────╮
        left_panel = QVBoxLayout()

        # ┌──────────────────────┐
        #   Preset selection box 
        # └──────────────────────┘
        create_group = QGroupBox("Create")
        create_layout = QVBoxLayout()
        
        # Type selector
        mode_layout = QHBoxLayout()
        self.radio_image = QRadioButton("Image (2x32)")
        self.radio_anim = QRadioButton("Animation (400x32)")
        self.radio_image.setChecked(True)
        self.radio_image.toggled.connect(self.update_preset_list)
        mode_layout.addWidget(self.radio_image)
        mode_layout.addWidget(self.radio_anim)

        create_layout.addLayout(mode_layout)
        

        # Preset selector
        self.preset_combo = QComboBox()
        self.preset_combo.currentIndexChanged.connect(self.load_preset_ui)
        
        create_layout.addWidget(self.preset_combo)
        

        create_group.setLayout(create_layout)
        left_panel.addWidget(create_group)

        # ┌──────────────────────────┐
        #   Preset configuration box 
        # └──────────────────────────┘
        self.config_group = QGroupBox("Configure")
        self.config_layout = QFormLayout()
        self.config_group.setLayout(self.config_layout)

        left_panel.addWidget(self.config_group)
        

        left_panel.addStretch()

        main_layout.addLayout(left_panel, 1)
    # ╰────────────────────────────────────────────────────────────────────╯

    # ╭─ Right panel: preview and export images ────────────────────────╮
        right_panel = QVBoxLayout()

        # ┌────────────────┐
        #   Preview window 
        # └────────────────┘
        preview_group = QGroupBox("Preview")
        preview_layout = QVBoxLayout()
        
        self.preview_label = QLabel("No preview")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("background-color: black;")
        self.preview_label.setMinimumSize(420, 100)
        
        preview_layout.addWidget(self.preview_label, 1) 

        # ┌────────────────────────────┐
        #   Animation preview controls 
        # └────────────────────────────┘
        anim_controls_layout = QHBoxLayout()
        
        # Static/animated preview switch
        self.anim_checkbox = QCheckBox("Play Animation")
        self.anim_checkbox.setEnabled(False)
        self.anim_checkbox.toggled.connect(self.render_preview)

        anim_controls_layout.addWidget(self.anim_checkbox)
        anim_controls_layout.addStretch() 
        
        # Animation speed slider
        self.speed_label = QLabel("1.00 s")
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        # Slider step is .01s
        self.speed_slider.setMinimum(10)   # .1s
        self.speed_slider.setMaximum(200)  # 2s
        self.speed_slider.setValue(100)  # 1s
        self.speed_slider.setEnabled(False)
        self.speed_slider.setFixedWidth(150) 
        self.speed_slider.valueChanged.connect(self.update_speed)


        anim_controls_layout.addWidget(QLabel("Playback Time:"))
        anim_controls_layout.addWidget(self.speed_slider)
        anim_controls_layout.addWidget(self.speed_label)

        preview_layout.addLayout(anim_controls_layout) 

        # ┌───────────────┐
        #   Export button 
        # └───────────────┘
        self.btn_save = QPushButton("Export as .BMP")
        self.btn_save.clicked.connect(self.export_bmp)

        preview_layout.addWidget(self.btn_save)

        
        preview_group.setLayout(preview_layout)

        right_panel.addWidget(preview_group)


        main_layout.addLayout(right_panel, 2)
    # ╰─────────────────────────────────────────────────────────────────╯

    # ╭─ Timer for animation ───────────────────────────╮
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick_animation)
    # ╰─────────────────────────────────────────────────╯


# ╭──────────────────────────────────────────────────────────╮
# │                   Preset list updater                    │
# │      (for when we switch "image" <--> "animation")       │
# ╰──────────────────────────────────────────────────────────╯
    def update_preset_list(self):
    # ╭─ Empty the list ──────────╮
        self.preset_combo.clear()
    # ╰───────────────────────────╯

    # ╭─ Determine current mode ────────────────────────────────────────╮
        mode = "image" if self.radio_image.isChecked() else "animation"
    # ╰─────────────────────────────────────────────────────────────────╯

    # ╭─ Configure animation preview ──────────────────────╮
        self.anim_checkbox.setEnabled(mode == "animation")
        if mode == "image":
            self.anim_checkbox.setChecked(False)
    # ╰────────────────────────────────────────────────────╯

    # ╭─ Add new presets to the list ──────────────────────────╮
        for preset in self.presets:
            if preset.mode == mode:
                self.preset_combo.addItem(preset.name, preset)
    # ╰────────────────────────────────────────────────────────╯


# ╭──────────────────────────────────────────────────────────╮
# │                 Preset controls generator                │
# ╰──────────────────────────────────────────────────────────╯
    def load_preset_ui(self):
        """Dynamically builds the UI based on the chosen preset's parameters."""
        
    # ╭─ Clear configuration window ─────────────╮
        while self.config_layout.rowCount() > 0:
            self.config_layout.removeRow(0)
    # ╰──────────────────────────────────────────╯

    # ╭─ Determine current preset ──────────────────────────────╮
        index = self.preset_combo.currentIndex()
        if index < 0: return

        self.current_preset = self.preset_combo.itemData(index)
        self.current_params = {}
    # ╰─────────────────────────────────────────────────────────╯

    # ╭─ Build configuration window ────────────────────────────────────────────────────────────────────╮
        for param in self.current_preset.params:
            key = param["key"]
            self.current_params[key] = param["default"]
            
            if param["type"] == "color":
                # ┌──────────────┐
                #   Color picker 
                # └──────────────┘
                btn = QPushButton("Choose Color")
                r, g, b = param["default"]
                # Adjust text color for contrast
                text_color = "black" if (r*0.299 + g*0.587 + b*0.114) > 186 else "white"
                btn.setStyleSheet(
                  f"background-color: rgb({r},{g},{b}); color: {text_color}; border: none;")
                btn.clicked.connect(lambda checked, k=key, b=btn: self.pick_color(k, b))
                self.config_layout.addRow(param["name"], btn)
                
            elif param["type"] == "int":
                # ┌────────┐
                #   Slider 
                # └────────┘
                slider = QSlider(Qt.Orientation.Horizontal)
                slider.setMinimum(param["min"])
                slider.setMaximum(param["max"])
                slider.setValue(param["default"])
                
                val_label = QLabel(str(param["default"]))
                slider.valueChanged.connect(lambda val, k=key, l=val_label: self.update_int(k, val, l))
                
                row_layout = QHBoxLayout()
                row_layout.addWidget(slider)
                row_layout.addWidget(val_label)
                self.config_layout.addRow(param["name"], row_layout)

            elif param["type"] == "choice":
                # ┌───────────┐
                #   Combo box 
                # └───────────┘
                combo = QComboBox()
                combo.addItems(param["options"])
                combo.setCurrentText(param["default"])
                combo.currentTextChanged.connect(lambda val, k=key: self.update_generic(k, val))
                self.config_layout.addRow(param["name"], combo)

            elif param["type"] == "bool":
                # ┌──────────┐
                #   Checkbox 
                # └──────────┘
                checkbox = QCheckBox()
                checkbox.setChecked(param["default"])
                checkbox.toggled.connect(lambda val, k=key: self.update_generic(k, val))
                self.config_layout.addRow(param["name"], checkbox)
    # ╰─────────────────────────────────────────────────────────────────────────────────────────────────╯

    # ╭─ Make preview ────────╮
        self.generate_image()
    # ╰───────────────────────╯


# ╭──────────────────────────────────────────────────────────╮
# │               Scripts for updating values                │
# ╰──────────────────────────────────────────────────────────╯
    def pick_color(self, key, btn):
    # ╭─ Color picker ─────────────────────────────────────────────────────────────────────╮
        # Read color from user
        color = QColorDialog.getColor()

        if color.isValid():
            # Convert to RGB
            r, g, b = color.red(), color.green(), color.blue()
            self.current_params[key] = (r, g, b)

            # Adjust placeholder color for contrast
            text_color = "black" if (r*0.299 + g*0.587 + b*0.114) > 186 else "white"

            # Restyle button
            btn.setStyleSheet(f"background-color: rgb({r},{g},{b}); color: {text_color};")

            # Update image preview
            self.generate_image()
    # ╰────────────────────────────────────────────────────────────────────────────────────╯

    def update_int(self, key, val, label):
    # ╭─ Number slider ────────────────╮
        # Read number
        self.current_params[key] = val

        # Change placeholder
        label.setText(str(val))

        # Update image preview
        self.generate_image()
    # ╰────────────────────────────────╯

    def update_generic(self, key, val):
    # ╭─ Combo box menu ───────────────╮
        # Read option
        self.current_params[key] = val

        # Update image preview
        self.generate_image()
    # ╰────────────────────────────────╯

    def generate_image(self):
    # ╭─ UI updater ─────────────────────────────────────────────────────────────────╮
        # Do nothing if something's wrong
        if not self.current_preset: return

        # Generate image from preset
        self.current_image_array = self.current_preset.generate(self.current_params)

        # Render image preview
        self.render_preview()
    # ╰──────────────────────────────────────────────────────────────────────────────╯

    def update_speed(self, val):
    # ╭─ Animation speed slider ─────────────────────╮
        # Update placeholder
        self.speed_label.setText(f"{val/100:.2f} s")

        if self.timer.isActive():
            # Update timer time step
            # ms delay = .01s * 10 / 400 frames
            self.timer.setInterval(int(val / 40))
    # ╰──────────────────────────────────────────────╯


# ╭──────────────────────────────────────────────────────────╮
# │                      Render preview                      │
# ╰──────────────────────────────────────────────────────────╯
    def render_preview(self):
        if self.current_image_array is None: return

        array_to_render = self.current_image_array

    # ╭─ Timer setup ───────────────────────────────────────────────────────────────────────────╮
        if self.anim_checkbox.isChecked():
            self.speed_slider.setEnabled(True)
            
            # If user has just toggled the checkbox
            if not self.timer.isActive():
                self.anim_frame = 0
                # Time measured in .01s intervals
                anim_time = self.speed_slider.value()  
                # Step in ms = .01s * 10 / 400 frames
                self.timer.start(int(anim_time / 40)) 

            # Slice the 400x32 array down to a 1x32 moving frame
            array_to_render = self.current_image_array[:, self.anim_frame:self.anim_frame+1, :]

        else:
            self.speed_slider.setEnabled(False)
            self.timer.stop()
    # ╰─────────────────────────────────────────────────────────────────────────────────────────╯

    # ╭─ Data preparation ──────────────────────────────────────────────────────────────────────╮
        height, width, channel = array_to_render.shape
        bytes_per_line = 3 * width
        
        # Convert the NumPy array to a standard contiguous bytes object
        image_bytes = array_to_render.tobytes()
        
        # Convert to QImage
        q_img = QImage(image_bytes, width, height, bytes_per_line, QImage.Format.Format_RGB888)
    # ╰─────────────────────────────────────────────────────────────────────────────────────────╯
        
    # ╭─ Scaling ─────────────────────────────────────────────────────────────────────╮
        if width > 2:
            # If it's the 400x32 static preview, squish it into a 600x100 rectangle
            scaled_img = q_img.scaled(600, 100, Qt.AspectRatioMode.IgnoreAspectRatio)
        else:
            # If it's a 1x32 or 2x32 image, make it tall and chunky
            scaled_img = q_img.scaled(60, 320, Qt.AspectRatioMode.IgnoreAspectRatio)
    # ╰───────────────────────────────────────────────────────────────────────────────╯
        
        self.preview_label.setPixmap(QPixmap.fromImage(scaled_img))


    def tick_animation(self):

        if self.current_image_array is None: return

    # ╭─ Select next frame ─────────────────────────────────────────────────────────╮
        self.anim_frame = (self.anim_frame + 1) % self.current_image_array.shape[1]
    # ╰─────────────────────────────────────────────────────────────────────────────╯
    # ╭─ Render it ───────────╮
        self.render_preview()
    # ╰───────────────────────╯



# ╭──────────────────────────────────────────────────────────╮
# │                    .bmp file exporter                    │
# ╰──────────────────────────────────────────────────────────╯
    def export_bmp(self):
        if self.current_image_array is None: return
        
        filename, _ = QFileDialog.getSaveFileName(self, "Save BMP", "", "BMP Files (*.bmp)")
        if filename:
            # Convert to bmp
            img = Image.fromarray(self.current_image_array)
            img.save(filename, format="BMP")
            print(f"Saved: {filename}")

