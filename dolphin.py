import dolphin_memory_engine as dme
import time

class Dolphin:
    def __init__(self, memory_cfg):
        self.action_address = int(memory_cfg["action_address"], 16)
        self.action_value = memory_cfg["action_value"]
        self.hooked = False

        # Map type strings to dme functions
        type_map = {
            "u8": (dme.read_byte, dme.write_byte),
            "u16": (dme.read_word, dme.write_word),
            "u32": (dme.read_word, dme.write_word),
            "float": (dme.read_float, dme.write_float),
            "double": (dme.read_double, dme.write_double)
        }
        _, self.write_func = type_map.get(memory_cfg.get("action_type", "u8"), (dme.read_byte, dme.write_byte))

    def hook(self, timeout=60):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                dme.hook()
                if dme.is_hooked():
                    self.hooked = True
                    print("\rDolphin hooked successfully!                     ")
                    return True
            except Exception:
                self.hooked = False
            remaining = int(timeout - (time.time() - start_time))
            print(f"\rWaiting for Dolphin to start... ({remaining}s left) ", end="")
            time.sleep(1)
        print("\nFailed to hook Dolphin.")
        return False

    def trigger_action(self):
        if not self.hooked:
            print("Cannot trigger action: Dolphin not hooked.")
            return
        try:
            self.write_func(self.action_address, self.action_value)
            print("Triggered local game action.")
        except Exception as e:
            print("Failed to trigger action:", e)
