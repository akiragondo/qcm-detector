from dataclasses import dataclass


@dataclass
class ConnectionParameters:
    port_name: str
    gate_time: int
    scale_factor: int
    simulation_data_path: str
    output_data_file: str

    def correct_metadata(self):
        return self.gate_time and self.scale_factor
