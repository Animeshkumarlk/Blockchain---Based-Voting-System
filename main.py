import hashlib
import time
import tkinter as tk
from tkinter import messagebox, font

# Blockchain class
class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash_value):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash_value = hash_value

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block", self.hash_block(0, "0", time.time(), "Genesis Block"))

    def hash_block(self, index, previous_hash, timestamp, data):
        value = f"{index}{previous_hash}{timestamp}{data}".encode()
        return hashlib.sha256(value).hexdigest()

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        latest_block = self.get_latest_block()
        new_block = Block(
            latest_block.index + 1,
            latest_block.hash_value,
            time.time(),
            data,
            self.hash_block(latest_block.index + 1, latest_block.hash_value, time.time(), data)
        )
        self.chain.append(new_block)

# Blockchain Voting System using Tkinter
class VotingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blockchain Voting System")
        self.root.configure(bg='#ffa500')  # Set background color
        self.blockchain = Blockchain()
        self.votes = {"Narendra Modi": 0, "Rahul Gandhi": 0}

        # Define bold font
        bold_font = font.Font(weight='bold')

        # Setup UI
        tk.Label(root, text="Select a candidate to vote for:", bg='#ffa500', font=bold_font).pack(pady=10)

        # Buttons with colors and bold text
        tk.Button(root, text="Vote for Narendra Modi", command=lambda: self.vote("Narendra Modi"), bg='#808080', fg='white', font=bold_font).pack(pady=5)
        tk.Button(root, text="Vote for Rahul Gandhi", command=lambda: self.vote("Rahul Gandhi"), bg='#808080', fg='white', font=bold_font).pack(pady=5)
        tk.Button(root, text="View Blockchain", command=self.view_blockchain, bg='#808080', fg='white', font=bold_font).pack(pady=5)
        tk.Button(root, text="View Vote Counts", command=self.view_votes, bg='#808080', fg='white', font=bold_font).pack(pady=5)

    def vote(self, candidate):
        if candidate in self.votes:
            self.votes[candidate] += 1
            self.blockchain.add_block(f"Vote for {candidate}")
            messagebox.showinfo("Vote", f"Your vote for {candidate} has been recorded!")
        else:
            messagebox.showerror("Error", "Invalid candidate!")

    def view_blockchain(self):
        blockchain_info = ""
        for block in self.blockchain.chain:
            blockchain_info += (
                f"Index: {block.index}\n"
                f"Previous Hash: {block.previous_hash}\n"
                f"Timestamp: {time.ctime(block.timestamp)}\n"
                f"Data: {block.data}\n"
                f"Hash: {block.hash_value}\n\n"
            )
        self.show_message("Blockchain", blockchain_info)

    def view_votes(self):
        vote_info = "\n".join(f"{candidate} Votes: {votes}" for candidate, votes in self.votes.items())
        self.show_message("Vote Counts", vote_info)

    def show_message(self, title, message):
        top = tk.Toplevel(self.root)
        top.title(title)
        tk.Message(top, text=message, font=font.Font(weight='bold')).pack(padx=10, pady=10)
        tk.Button(top, text="Close", command=top.destroy, bg='#808080', fg='white').pack(pady=5)

# Main Function
if __name__ == "__main__":
    root = tk.Tk()
    app = VotingApp(root)
    root.mainloop()
