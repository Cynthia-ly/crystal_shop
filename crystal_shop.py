import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crystal_shop.log'),
        logging.StreamHandler()
    ]
)

class Crystal:
    def __init__(self, name, price, quantity, description=""):
        self.name = name
        self.price = float(price)
        self.quantity = int(quantity)
        self.description = description
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"Created new crystal: {self.name}")

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "description": self.description,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        crystal = cls(
            data["name"],
            data["price"],
            data["quantity"],
            data["description"]
        )
        crystal.created_at = data["created_at"]
        return crystal

class CrystalShop:
    def __init__(self):
        self.crystals = {}
        self.data_file = "crystal_shop_data.json"
        self.load_data()
        logging.info("Crystal shop initialized")

    def add_crystal(self, name, price, quantity, description=""):
        try:
            if name in self.crystals:
                raise ValueError(f"水晶 {name} 已存在")
            if float(price) <= 0:
                raise ValueError("价格必须大于0")
            if int(quantity) <= 0:
                raise ValueError("数量必须大于0")
            
            self.crystals[name] = Crystal(name, price, quantity, description)
            self.save_data()
            logging.info(f"Added crystal: {name}")
            return True
        except Exception as e:
            logging.error(f"Error adding crystal: {str(e)}")
            raise

    def remove_crystal(self, name):
        try:
            if name not in self.crystals:
                raise ValueError(f"水晶 {name} 不存在")
            del self.crystals[name]
            self.save_data()
            logging.info(f"Removed crystal: {name}")
            return True
        except Exception as e:
            logging.error(f"Error removing crystal: {str(e)}")
            raise

    def update_crystal(self, name, price=None, quantity=None, description=None):
        try:
            if name not in self.crystals:
                raise ValueError(f"水晶 {name} 不存在")
            
            crystal = self.crystals[name]
            if price is not None:
                if float(price) <= 0:
                    raise ValueError("价格必须大于0")
                crystal.price = float(price)
            if quantity is not None:
                if int(quantity) < 0:
                    raise ValueError("数量不能为负数")
                crystal.quantity = int(quantity)
            if description is not None:
                crystal.description = description
            
            self.save_data()
            logging.info(f"Updated crystal: {name}")
            return True
        except Exception as e:
            logging.error(f"Error updating crystal: {str(e)}")
            raise

    def get_crystal(self, name):
        try:
            if name not in self.crystals:
                raise ValueError(f"水晶 {name} 不存在")
            return self.crystals[name]
        except Exception as e:
            logging.error(f"Error getting crystal: {str(e)}")
            raise

    def list_crystals(self):
        return list(self.crystals.values())

    def save_data(self):
        try:
            data = {name: crystal.to_dict() for name, crystal in self.crystals.items()}
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logging.info("Data saved successfully")
        except Exception as e:
            logging.error(f"Error saving data: {str(e)}")
            raise

    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.crystals = {name: Crystal.from_dict(crystal_data) 
                               for name, crystal_data in data.items()}
                logging.info("Data loaded successfully")
        except Exception as e:
            logging.error(f"Error loading data: {str(e)}")
            self.crystals = {}

class CrystalShopUI:
    def __init__(self, root):
        self.root = root
        self.root.title("水晶商店管理系统")
        self.root.geometry("800x600")
        self.shop = CrystalShop()
        self.setup_ui()
        logging.info("UI initialized")

    def setup_ui(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 创建输入框架
        input_frame = ttk.LabelFrame(main_frame, text="水晶信息", padding="5")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # 名称输入
        ttk.Label(input_frame, text="名称:").grid(row=0, column=0, sticky=tk.W)
        self.name_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.name_var).grid(row=0, column=1, sticky=(tk.W, tk.E))

        # 价格输入
        ttk.Label(input_frame, text="价格:").grid(row=1, column=0, sticky=tk.W)
        self.price_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.price_var).grid(row=1, column=1, sticky=(tk.W, tk.E))

        # 数量输入
        ttk.Label(input_frame, text="数量:").grid(row=2, column=0, sticky=tk.W)
        self.quantity_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.quantity_var).grid(row=2, column=1, sticky=(tk.W, tk.E))

        # 描述输入
        ttk.Label(input_frame, text="描述:").grid(row=3, column=0, sticky=tk.W)
        self.description_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.description_var).grid(row=3, column=1, sticky=(tk.W, tk.E))

        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=5)

        # 添加按钮
        ttk.Button(button_frame, text="添加水晶", command=self.add_crystal).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="删除水晶", command=self.remove_crystal).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="更新水晶", command=self.update_crystal).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="查询水晶", command=self.get_crystal).grid(row=0, column=3, padx=5)

        # 创建表格
        self.tree = ttk.Treeview(main_frame, columns=("name", "price", "quantity", "description", "created_at"),
                                show="headings")
        self.tree.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # 设置列标题
        self.tree.heading("name", text="名称")
        self.tree.heading("price", text="价格")
        self.tree.heading("quantity", text="数量")
        self.tree.heading("description", text="描述")
        self.tree.heading("created_at", text="创建时间")

        # 设置列宽
        self.tree.column("name", width=100)
        self.tree.column("price", width=100)
        self.tree.column("quantity", width=100)
        self.tree.column("description", width=200)
        self.tree.column("created_at", width=150)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=2, column=2, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)

        # 绑定双击事件
        self.tree.bind("<Double-1>", self.on_tree_double_click)

        # 更新显示
        self.update_tree()

    def update_tree(self):
        # 清空表格
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 添加数据
        for crystal in self.shop.list_crystals():
            self.tree.insert("", "end", values=(
                crystal.name,
                f"¥{crystal.price:.2f}",
                crystal.quantity,
                crystal.description,
                crystal.created_at
            ))

    def add_crystal(self):
        try:
            name = self.name_var.get().strip()
            price = self.price_var.get().strip()
            quantity = self.quantity_var.get().strip()
            description = self.description_var.get().strip()

            if not all([name, price, quantity]):
                messagebox.showerror("错误", "请填写所有必填字段")
                return

            self.shop.add_crystal(name, price, quantity, description)
            self.update_tree()
            self.clear_inputs()
            messagebox.showinfo("成功", f"水晶 {name} 添加成功")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def remove_crystal(self):
        try:
            name = self.name_var.get().strip()
            if not name:
                messagebox.showerror("错误", "请输入要删除的水晶名称")
                return

            if messagebox.askyesno("确认", f"确定要删除水晶 {name} 吗？"):
                self.shop.remove_crystal(name)
                self.update_tree()
                self.clear_inputs()
                messagebox.showinfo("成功", f"水晶 {name} 删除成功")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def update_crystal(self):
        try:
            name = self.name_var.get().strip()
            price = self.price_var.get().strip()
            quantity = self.quantity_var.get().strip()
            description = self.description_var.get().strip()

            if not name:
                messagebox.showerror("错误", "请输入要更新的水晶名称")
                return

            self.shop.update_crystal(
                name,
                price if price else None,
                quantity if quantity else None,
                description if description else None
            )
            self.update_tree()
            self.clear_inputs()
            messagebox.showinfo("成功", f"水晶 {name} 更新成功")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def get_crystal(self):
        try:
            name = self.name_var.get().strip()
            if not name:
                messagebox.showerror("错误", "请输入要查询的水晶名称")
                return

            crystal = self.shop.get_crystal(name)
            self.price_var.set(str(crystal.price))
            self.quantity_var.set(str(crystal.quantity))
            self.description_var.set(crystal.description)
            messagebox.showinfo("查询结果", f"水晶 {name} 查询成功")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def on_tree_double_click(self, event):
        try:
            item = self.tree.selection()[0]
            values = self.tree.item(item)["values"]
            self.name_var.set(values[0])
            self.price_var.set(values[1].replace("¥", ""))
            self.quantity_var.set(values[2])
            self.description_var.set(values[3])
        except Exception as e:
            logging.error(f"Error in tree double click: {str(e)}")

    def clear_inputs(self):
        self.name_var.set("")
        self.price_var.set("")
        self.quantity_var.set("")
        self.description_var.set("")

def main():
    try:
        root = tk.Tk()
        app = CrystalShopUI(root)
        root.mainloop()
    except Exception as e:
        logging.error(f"Application error: {str(e)}")
        messagebox.showerror("错误", f"应用程序发生错误: {str(e)}")

if __name__ == "__main__":
    main() 