import json
import os
from datetime import datetime, date
from typing import Optional
import pandas as pd


KATEGORI_PENGELUARAN = [
    "🍔 Makanan & Minuman",
    "🚗 Transportasi",
    "🏠 Tempat Tinggal",
    "💡 Tagihan & Utilitas",
    "🛒 Belanja",
    "🎮 Hiburan",
    "💊 Kesehatan",
    "📚 Pendidikan",
    "👔 Pakaian",
    "💰 Tabungan & Investasi",
    "🎁 Donasi & Hadiah",
    "📦 Lainnya"
]

SUMBER_PEMASUKAN = [
    "💼 Gaji",
    "💻 Freelance",
    "📈 Investasi",
    "🏪 Bisnis",
    "🎁 Hadiah/Bonus",
    "📦 Lainnya"
]


class FinanceManager:
    """Mengelola data keuangan pribadi (pemasukan & pengeluaran)."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.data_file = os.path.join(data_dir, "transactions.json")
        self.transactions = []
        self._ensure_data_dir()
        self._load_data()

    def _ensure_data_dir(self):
        """Buat direktori data jika belum ada."""
        os.makedirs(self.data_dir, exist_ok=True)

    def _load_data(self):
        """Load data transaksi dari file JSON."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.transactions = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.transactions = []
        else:
            self.transactions = []

    def _save_data(self):
        """Simpan data transaksi ke file JSON."""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.transactions, f, ensure_ascii=False, indent=2, default=str)

    def tambah_pemasukan(self, jumlah: float, sumber: str, tanggal: str,
                         catatan: str = "") -> dict:
        """Tambah transaksi pemasukan."""
        transaksi = {
            "id": len(self.transactions) + 1,
            "tipe": "pemasukan",
            "jumlah": jumlah,
            "kategori": sumber,
            "tanggal": tanggal,
            "catatan": catatan,
            "created_at": datetime.now().isoformat()
        }
        self.transactions.append(transaksi)
        self._save_data()
        return transaksi

    def tambah_pengeluaran(self, jumlah: float, kategori: str, tanggal: str,
                           catatan: str = "") -> dict:
        """Tambah transaksi pengeluaran."""
        transaksi = {
            "id": len(self.transactions) + 1,
            "tipe": "pengeluaran",
            "jumlah": jumlah,
            "kategori": kategori,
            "tanggal": tanggal,
            "catatan": catatan,
            "created_at": datetime.now().isoformat()
        }
        self.transactions.append(transaksi)
        self._save_data()
        return transaksi

    def hapus_transaksi(self, transaction_id: int) -> bool:
        """Hapus transaksi berdasarkan ID."""
        for i, t in enumerate(self.transactions):
            if t["id"] == transaction_id:
                self.transactions.pop(i)
                self._save_data()
                return True
        return False

    def get_semua_transaksi(self) -> list:
        """Ambil semua transaksi."""
        return self.transactions

    def get_pemasukan(self) -> list:
        """Ambil semua transaksi pemasukan."""
        return [t for t in self.transactions if t["tipe"] == "pemasukan"]

    def get_pengeluaran(self) -> list:
        """Ambil semua transaksi pengeluaran."""
        return [t for t in self.transactions if t["tipe"] == "pengeluaran"]

    def total_pemasukan(self) -> float:
        """Hitung total pemasukan."""
        return sum(t["jumlah"] for t in self.get_pemasukan())

    def total_pengeluaran(self) -> float:
        """Hitung total pengeluaran."""
        return sum(t["jumlah"] for t in self.get_pengeluaran())

    def saldo(self) -> float:
        """Hitung saldo (pemasukan - pengeluaran)."""
        return self.total_pemasukan() - self.total_pengeluaran()

    def pengeluaran_per_kategori(self) -> dict:
        """Hitung total pengeluaran per kategori."""
        result = {}
        for t in self.get_pengeluaran():
            kat = t["kategori"]
            result[kat] = result.get(kat, 0) + t["jumlah"]
        return result

    def pemasukan_per_sumber(self) -> dict:
        """Hitung total pemasukan per sumber."""
        result = {}
        for t in self.get_pemasukan():
            src = t["kategori"]
            result[src] = result.get(src, 0) + t["jumlah"]
        return result

    def tren_bulanan(self) -> pd.DataFrame:
        """Hitung tren pemasukan dan pengeluaran bulanan."""
        if not self.transactions:
            return pd.DataFrame(columns=["Bulan", "Pemasukan", "Pengeluaran"])

        df = pd.DataFrame(self.transactions)
        df["tanggal"] = pd.to_datetime(df["tanggal"])
        df["bulan"] = df["tanggal"].dt.to_period("M").astype(str)

        pemasukan = df[df["tipe"] == "pemasukan"].groupby("bulan")["jumlah"].sum()
        pengeluaran = df[df["tipe"] == "pengeluaran"].groupby("bulan")["jumlah"].sum()

        semua_bulan = sorted(set(pemasukan.index) | set(pengeluaran.index))

        result = pd.DataFrame({
            "Bulan": semua_bulan,
            "Pemasukan": [pemasukan.get(b, 0) for b in semua_bulan],
            "Pengeluaran": [pengeluaran.get(b, 0) for b in semua_bulan]
        })
        return result

    def ringkasan_keuangan(self) -> dict:
        """Buat ringkasan keuangan lengkap untuk AI advisor."""
        total_in = self.total_pemasukan()
        total_out = self.total_pengeluaran()
        saldo = self.saldo()

        # Rasio pengeluaran
        rasio = (total_out / total_in * 100) if total_in > 0 else 0

        # Pengeluaran terbesar
        per_kat = self.pengeluaran_per_kategori()
        kategori_terbesar = max(per_kat, key=per_kat.get) if per_kat else "-"

        # Jumlah transaksi
        jml_transaksi = len(self.transactions)

        return {
            "total_pemasukan": total_in,
            "total_pengeluaran": total_out,
            "saldo": saldo,
            "rasio_pengeluaran": round(rasio, 1),
            "pengeluaran_per_kategori": per_kat,
            "pemasukan_per_sumber": self.pemasukan_per_sumber(),
            "kategori_terbesar": kategori_terbesar,
            "jumlah_transaksi": jml_transaksi
        }

    def to_dataframe(self) -> pd.DataFrame:
        """Konversi transaksi ke DataFrame."""
        if not self.transactions:
            return pd.DataFrame(columns=["ID", "Tipe", "Jumlah", "Kategori", "Tanggal", "Catatan"])

        df = pd.DataFrame(self.transactions)
        df = df.rename(columns={
            "id": "ID",
            "tipe": "Tipe",
            "jumlah": "Jumlah",
            "kategori": "Kategori",
            "tanggal": "Tanggal",
            "catatan": "Catatan"
        })
        df = df[["ID", "Tipe", "Jumlah", "Kategori", "Tanggal", "Catatan"]]
        df["Tanggal"] = pd.to_datetime(df["Tanggal"]).dt.strftime("%d %b %Y")
        df["Jumlah"] = df.apply(
            lambda row: f"Rp {row['Jumlah']:,.0f}", axis=1
        )
        return df.sort_values("ID", ascending=False).reset_index(drop=True)

    def export_csv(self) -> str:
        """Export transaksi ke format CSV string."""
        df = self.to_dataframe()
        return df.to_csv(index=False)
