import pandas
import matplotlib.pyplot as plt
import numpy as np

xls = pandas.ExcelFile('dataset1.xlsx')
mahasiswaDataset = pandas.read_excel(xls, 'Daftar mahasiswa baru', dtype={'NPM': str})
yudisiumDataset = pandas.read_excel(xls, 'Yudisium 2014-2023')[['NPM', 'Nama Lulusan', 'kode_lulus']]

# A. menentukan jumlah program studi
programStudi = mahasiswaDataset.groupby(['Program Studi']).size()
# print('{}\nBanyak Program Studi: {}'.format(programStudi, len(programStudi)))

# B. Lakukan tabulasi data atau kelengkapan data untuk menjawab pertanyaan apakah seluruh mahasiswa baru tersebut lulus
# expected outputs:
#   - jumlah mhs tidak lulus
#   - jumlah mhs lulus
npms = mahasiswaDataset[['NPM', 'Program Studi']].copy()
yudisiumFilteredDataset = yudisiumDataset[['NPM', 'Nama Lulusan', 'kode_lulus']].copy()

# transformation, clear dot separators
yudisiumFilteredDataset['NPM'] = yudisiumFilteredDataset['NPM'].str.replace('.', '', regex=False).astype('string')
mhsGradudated = pandas.merge(yudisiumFilteredDataset, npms, on=['NPM'])
# perform left join / anti join
mhsNotGradudated = pandas.merge(mahasiswaDataset, mhsGradudated['NPM'], how='left', on=['NPM'], indicator=True).query('_merge=="left_only"')

# C. Plot

mhsSize = mahasiswaDataset.groupby(['Program Studi']).size().reset_index(name='Jumlah Mahasiswa')
mhsGradudatedSize = mhsGradudated.groupby(['Program Studi']).size().reset_index(name='Jumlah Mahasiswa Lulus')
mhsNotGradudatedSize = mhsNotGradudated.groupby(['Program Studi']).size().reset_index(name='Mahasiswa Tidak Lulus')

a = pandas.merge(mhsSize, mhsGradudatedSize, on=['Program Studi'])
data = pandas.merge(a, mhsNotGradudatedSize, on=['Program Studi'])

print("\n{}".format(data.head))

# Generate positions for bars
x = np.arange(len(data['Program Studi']))

# Set bar width
bar_width = 0.35

plt.bar(data['Program Studi'], data['Jumlah Mahasiswa Lulus'], label='Mahasiswa Lulus', color='green')
plt.bar(data['Program Studi'], data['Mahasiswa Tidak Lulus'], label='Mahasiswa Tidak Lulus', bottom=data['Jumlah Mahasiswa Lulus'], color='red')

# Add labels and title
plt.xlabel('Program Studi', fontsize=12)
plt.ylabel('Jumlah Mahasiswa', fontsize=12)
plt.title('Distribusi Kelulusan Mahasiswa per Program Studi', fontsize=16)
plt.xticks(x, data['Program Studi'], rotation=45, ha='right', fontsize=10)
plt.legend()

# Show plot
plt.tight_layout()
plt.show()