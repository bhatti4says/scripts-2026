import curses
import re

# ==========================================
# PHASE 1: THE CORE ENGINE (Paste here)
# ==========================================
class ProjectPlannerEngine:
    def __init__(self, rows=20, cols=10):
        self.rows = rows
        self.cols = cols
        self.cells = {} 

    def get_cell_label(self, r, c):
        return f"{chr(65 + c)}{r + 1}"

    def get_value(self, cell_label):
        raw = self.cells.get(cell_label, "")
        if not raw:
            return 0
        if str(raw).startswith('='):
            return self.evaluate_formula(raw[1:])
        try:
            return float(raw) if '.' in str(raw) else int(raw)
        except ValueError:
            return raw

    def evaluate_formula(self, formula):
        cell_refs = re.findall(r'[A-Z]+\d+', formula)
        evaluated_formula = formula
        for ref in cell_refs:
            val = self.get_value(ref)
            evaluated_formula = evaluated_formula.replace(ref, str(val))
        try:
            return eval(evaluated_formula, {"__builtins__": None}, {})
        except Exception:
            return "#ERR!"

# ==========================================
# PHASE 2: THE UI FUNCTIONS (Paste here)
# ==========================================
def draw_grid(stdscr, engine, start_row, start_col, active_r, active_c, input_mode, current_input):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    current_label = engine.get_cell_label(active_r, active_c)
    raw_val = engine.cells.get(current_label, "")
    mode_str = "[EDIT]" if input_mode else "[NAV]"
    stdscr.addstr(0, 0, f"{mode_str} {current_label}: {raw_val:<30}", curses.A_REVERSE)
    if input_mode:
        stdscr.addstr(1, 0, f"Editing: {current_input}", curses.A_BOLD)
    else:
        stdscr.addstr(1, 0, "Use Arrow Keys to navigate. Press 'Enter' or 'F2' to Edit. 'ESC' to cancel.")

    cell_width = 12
    start_y = 3

    for c in range(engine.cols):
        stdscr.addstr(start_y, (c * cell_width) + 4, f"{chr(65 + c):^10}", curses.A_UNDERLINE)

    for r in range(engine.rows):
        stdscr.addstr(start_y + 1 + r, 0, f"{r+1:>3} |")
        for c in range(engine.cols):
            label = engine.get_cell_label(r, c)
            val = engine.get_value(label)
            display_str = f"{str(val)[:cell_width-2]:^10}"
            x_pos = (c * cell_width) + 5
            y_pos = start_y + 1 + r
            
            if r == active_r and c == active_c:
                stdscr.addstr(y_pos, x_pos, display_str, curses.A_REVERSE)
            else:
                stdscr.addstr(y_pos, x_pos, display_str)
    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0) 
    stdscr.keypad(True)
    
    engine = ProjectPlannerEngine(rows=15, cols=6)
    active_r, active_c = 0, 0
    input_mode = False
    current_input = ""

    while True:
        draw_grid(stdscr, engine, 0, 0, active_r, active_c, input_mode, current_input)
        ch = stdscr.getch()

        if input_mode:
            if ch in (10, 13):  
                label = engine.get_cell_label(active_r, active_c)
                engine.cells[label] = current_input
                input_mode = False
                current_input = ""
                if active_r < engine.rows - 1: active_r += 1
            elif ch == 27:  
                input_mode = False
                current_input = ""
            elif ch in (curses.KEY_BACKSPACE, 127, 8): 
                current_input = current_input[:-1]
            elif 32 <= ch <= 126:  
                current_input += chr(ch)
        else:
            if ch == curses.KEY_UP and active_r > 0:
                active_r -= 1
            elif ch == curses.KEY_DOWN and active_r < engine.rows - 1:
                active_r += 1
            elif ch == curses.KEY_LEFT and active_c > 0:
                active_c -= 1
            elif ch == curses.KEY_RIGHT and active_c < engine.cols - 1:
                active_c += 1
            elif ch in (10, 13, curses.KEY_F2):  
                input_mode = True
                current_input = str(engine.cells.get(engine.get_cell_label(active_r, active_c), ""))
            elif ch == ord('q'):  
                break

if __name__ == "__main__":
    curses.wrapper(main)
