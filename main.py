import time
import tkinter as tk
from tkinter import messagebox

# ===================== AVL TREE CORE =====================

def create_node(value):
    return {
        'value': value,
        'left': None,
        'right': None,
        'height': 0
    }

def get_height(node):
    if node is None:
        return -1
    return node['height']

def balance_factor(node):
    if node is None:
        return 0
    return get_height(node['left']) - get_height(node['right'])

def rotate_right(old_node):
    node = old_node['left']
    temp = node['right']

    node['right'] = old_node
    old_node['left'] = temp

    old_node['height'] = max(get_height(old_node['left']), get_height(old_node['right'])) + 1
    node['height'] = max(get_height(node['left']), get_height(node['right'])) + 1

    return node

def rotate_left(old_node):
    node = old_node['right']
    temp = node['left']

    node['left'] = old_node
    old_node['right'] = temp

    old_node['height'] = max(get_height(old_node['left']), get_height(old_node['right'])) + 1
    node['height'] = max(get_height(node['left']), get_height(node['right'])) + 1

    return node

def insert(node, value):
    msg = None
    if node is None:
        return create_node(value), msg

    if value < node['value']:
        node['left'], msg = insert(node['left'], value)
    elif value > node['value']:
        node['right'], msg = insert(node['right'], value)
    else:
        return node, msg

    node['height'] = max(get_height(node['left']), get_height(node['right'])) + 1
    balance = balance_factor(node)

    if balance > 1 and value < node['left']['value']:
        msg = f"Imbalance! Left-Left Rotation applied at {node['value']}"
        return rotate_right(node), msg

    if balance > 1 and value > node['left']['value']:
        msg = f"Imbalance! Left-Right Rotation applied at {node['value']}"
        node['left'] = rotate_left(node['left'])
        return rotate_right(node), msg

    if balance < -1 and value > node['right']['value']:
        msg = f"Imbalance! Right-Right Rotation applied at {node['value']}"
        return rotate_left(node), msg

    if balance < -1 and value < node['right']['value']:
        msg = f"Imbalance! Right-Left Rotation applied at {node['value']}"
        node['right'] = rotate_right(node['right'])
        return rotate_left(node), msg

    return node, msg

def min_value_node(node):
    current = node
    while current['right'] is not None:
        current = current['right']
    return current

def delete(node, value):
    msg = None
    if node is None:
        return node, msg

    if value < node['value']:
        node['left'], msg = delete(node['left'], value)
    elif value > node['value']:
        node['right'], msg = delete(node['right'], value)
    else:
        if node['left'] is None:
            temp = node['right']
            node = None
            return temp, msg
        elif node['right'] is None:
            temp = node['left']
            node = None
            return temp, msg

        temp = min_value_node(node['left'])
        node['value'] = temp['value']
        node['left'], msg = delete(node['left'], temp['value'])

    if node is None:
        return node, msg

    node['height'] = max(get_height(node['left']), get_height(node['right'])) + 1
    balance = balance_factor(node)

    if balance > 1 and balance_factor(node['left']) >= 0:
        msg = f"After deletion: Left-Left Rotation at {node['value']}"
        return rotate_right(node), msg

    if balance > 1 and balance_factor(node['left']) < 0:
        msg = f"After deletion: Left-Right Rotation at {node['value']}"
        node['left'] = rotate_left(node['left'])
        return rotate_right(node), msg

    if balance < -1 and balance_factor(node['right']) <= 0:
        msg = f"After deletion: Right-Right Rotation at {node['value']}"
        return rotate_left(node), msg

    if balance < -1 and balance_factor(node['right']) > 0:
        msg = f"After deletion: Right-Left Rotation at {node['value']}"
        node['right'] = rotate_right(node['right'])
        return rotate_left(node), msg

    return node, msg

def search(node, value):
    if node is None or node['value'] == value:
        return node
    if value < node['value']:
        return search(node['left'], value)
    return search(node['right'], value)

# ===================== TRAVERSALS =====================

def inorder(node, result=None):
    if result is None:
        result = []
    if node:
        inorder(node['left'], result)
        result.append(node['value'])
        inorder(node['right'], result)
    return result

def preorder(node, result=None):
    if result is None:
        result = []
    if node:
        result.append(node['value'])
        preorder(node['left'], result)
        preorder(node['right'], result)
    return result

def postorder(node, result=None):
    if result is None:
        result = []
    if node:
        postorder(node['left'], result)
        postorder(node['right'], result)
        result.append(node['value'])
    return result

# ===================== VISUALIZATION =====================

def calculate_positions(node, x, y, level_width):
    positions = {}
    if node is None:
        return positions

    canvas_width = 990
    if node == tree:
        x = canvas_width // 2

    positions[node['value']] = (x, y)

    if node['left'] is not None:
        new_x = max(x - level_width, node_radius + 10)
        positions.update(
            calculate_positions(node['left'], new_x, y + vertical_spacing, level_width * 0.65)
        )

    if node['right'] is not None:
        new_x = min(x + level_width, canvas_width - node_radius - 10)
        positions.update(
            calculate_positions(node['right'], new_x, y + vertical_spacing, level_width * 0.65)
        )

    return positions

def draw_edges(node, positions, parent_pos=None):
    if node is None:
        return

    node_pos = positions.get(node['value'])
    if node_pos is None:
        return

    x, y = node_pos

    if parent_pos is not None:
        px, py = parent_pos
        canvas.create_line(px, py + node_radius / 2, x, y - node_radius / 2,
                           fill='#2c3e50', width=2, smooth=True)

    draw_edges(node['left'], positions, (x, y))
    draw_edges(node['right'], positions, (x, y))

def draw_node(x, y, value):
    node_obj = search(tree, value)
    if node_obj:
        bf = abs(balance_factor(node_obj))
        color = '#57a8de' if bf == 0 else '#4ce68d'
    else:
        color = '#57a8de'

    canvas.create_oval(
        x - node_radius / 2, y - node_radius / 2,
        x + node_radius / 2, y + node_radius / 2,
        fill=color, outline='#2c3e50', width=2
    )

    canvas.create_text(x, y, text=str(value),
                       font=('Arial', 12, 'bold'), fill='white')

    if node_obj:
        canvas.create_text(x, y + 10 + node_radius / 2,
                           text=f"BF:{abs(balance_factor(node_obj))}",
                           font=('Arial', 9), fill='#7f8c8d')
        canvas.create_text(x, y - 10 - node_radius / 2,
                           text=f"H:{node_obj['height']}",
                           font=('Arial', 9), fill='#7f8c8d')

def draw_tree():
    canvas.delete("all")

    if tree is None:
        canvas.create_text(490, 225, text="AVL Tree is Empty",
                           font=('Arial', 18, 'bold'), fill='#95a5a6')
        canvas.create_text(490, 260,
                           text="Start by inserting a value...",
                           font=('Arial', 12), fill='#bdc3c7')
        return

    positions = calculate_positions(tree, 490, 50, 180)
    draw_edges(tree, positions)

    for value, (x, y) in positions.items():
        draw_node(x, y, value)

    canvas.create_rectangle(10, 420, 970, 445,
                            fill='#ecf0f1', outline='#bdc3c7')
    canvas.create_text(490, 432,
                       text=f"Total Nodes: {len(positions)} | Tree Height: {tree['height']}",
                       font=('Arial', 10, 'bold'), fill='#2c3e50')

# ===================== UI ACTIONS =====================

def ui_insert():
    global tree
    try:
        value = int(value_entry.get())
        if search(tree, value):
            messagebox.showinfo("Info", f"{value} already exists in the tree!")
            return

        tree, msg = insert(tree, value)
        value_entry.delete(0, tk.END)
        draw_tree()

        if msg:
            messagebox.showinfo("Rotation", msg)
        else:
            info_label.config(text=f"{value} inserted successfully.")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number!")

def ui_delete():
    global tree
    try:
        value = int(value_entry.get())
        if not search(tree, value):
            messagebox.showinfo("Info", f"{value} not found in the tree!")
            return

        tree, msg = delete(tree, value)
        value_entry.delete(0, tk.END)
        draw_tree()

        if msg:
            messagebox.showinfo("Rotation", msg)

        info_label.config(text=f"{value} deleted.")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number!")

def ui_search():
    try:
        value = int(value_entry.get())
        node = search(tree, value)
        value_entry.delete(0, tk.END)

        if node:
            messagebox.showinfo(
                "Search Result",
                f"{value} found!\nHeight: {node['height']}\nBalance Factor: {abs(balance_factor(node))}"
            )
        else:
            messagebox.showinfo("Search Result", f"{value} not found!")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number!")

def clear_tree():
    global tree
    tree = None
    draw_tree()
    info_label.config(text="Tree cleared. You can insert new values.")

def show_inorder():
    if tree is None:
        messagebox.showinfo("Inorder", "TREE IS EMPTY!")
    else:
        messagebox.showinfo("Inorder Traversal", " → ".join(map(str, inorder(tree))))

def show_preorder():
    if tree is None:
        messagebox.showinfo("Preorder", "TREE IS EMPTY!")
    else:
        messagebox.showinfo("Preorder Traversal", " → ".join(map(str, preorder(tree))))

def show_postorder():
    if tree is None:
        messagebox.showinfo("Postorder", "TREE IS EMPTY!")
    else:
        messagebox.showinfo("Postorder Traversal", " → ".join(map(str, postorder(tree))))

def sample_tree():
    global tree
    tree = None
    data = [14, 17, 11, 7, 53, 4, 13, 12, 8]
    for v in data:
        tree, _ = insert(tree, v)
    draw_tree()
    info_label.config(text=f"Sample tree created with {len(data)} nodes.")

# ===================== WINDOW SETUP =====================

def create_window():
    window = tk.Tk()
    window.title("AVL TREE SIMULATION")
    window.geometry("1100x700")
    window.configure(bg='#f0f8ff')
    return window

def add_title(window):
    title = tk.Label(
        window,
        text="AVL TREE SIMULATION",
        font=('Arial', 20, 'bold'),
        bg='#f0f8ff',
        fg='#000080'
    )
    title.pack(pady=10)

def create_canvas(window):
    global canvas
    canvas = tk.Canvas(
        window,
        width=990,
        height=450,
        bg='white',
        highlightthickness=1,
        highlightbackground='#bdc3c7'
    )
    canvas.pack(pady=10)
    if tree is None:
        canvas.create_text(490, 225, text="AVL Tree is Empty", font=('Arial', 18, 'bold'), fill='#95a5a6')
        canvas.create_text(490, 260,text="Start by inserting a value... ",font=('Arial', 12),fill='#bdc3c7')
    return canvas

def control_panel(window):
    global value_entry
    bg = '#e6f2ff'

    panel = tk.Frame(window, bg=bg)
    panel.pack(pady=10)

    entry_frame = tk.Frame(panel, bg=bg)
    entry_frame.pack(pady=5)

    tk.Label(entry_frame, text="Value:", font=('Arial', 11), bg=bg).pack(side="left", padx=5)

    value_entry = tk.Entry(entry_frame, font=('Arial', 12),
                            width=12, justify='center', bd=2, relief="sunken")
    value_entry.pack(side="left", padx=5)
    value_entry.bind('<Return>', lambda e: ui_insert())

    btn_frame1 = tk.Frame(panel, bg=bg)
    btn_frame1.pack(pady=5)

    tk.Button(btn_frame1, text="Insert", command=ui_insert,
              bg='#70c488', fg='white', width=8).pack(side="left", padx=3)
    tk.Button(btn_frame1, text="Delete", command=ui_delete,
              bg='#c7505b', fg='white', width=8).pack(side="left", padx=3)
    tk.Button(btn_frame1, text="Search", command=ui_search,
              bg='#4869b8', fg='white', width=8).pack(side="left", padx=3)

    btn_frame2 = tk.Frame(panel, bg=bg)
    btn_frame2.pack(pady=5)

    tk.Button(btn_frame2, text="Inorder", command=show_inorder,
              bg='#aa90e8', fg='white', width=10).pack(side="left", padx=3)
    tk.Button(btn_frame2, text="Preorder", command=show_preorder,
              bg='#aa90e8', fg='white', width=10).pack(side="left", padx=3)
    tk.Button(btn_frame2, text="Postorder", command=show_postorder,
              bg='#aa90e8', fg='white', width=10).pack(side="left", padx=3)
    tk.Button(btn_frame2, text="Clear", command=clear_tree,
              bg='#a39f9b', fg='white', width=8).pack(side="left", padx=3)
    tk.Button(btn_frame2, text="Sample Tree", command=sample_tree,
              bg='#de984e', fg='white', width=12).pack(side="left", padx=3)

# ===================== GLOBALS & START =====================

tree = None
value_entry = None
node_radius = 60
vertical_spacing = 90

window = create_window()
add_title(window)
create_canvas(window)
control_panel(window)

info_label = tk.Label(
    window,
    text="Welcome to AVL Tree Simulation!",
    font=('Arial', 12),
    bg='#f0f8ff',
    fg='#2c3e50'
)
info_label.pack(pady=10)

window.mainloop()

