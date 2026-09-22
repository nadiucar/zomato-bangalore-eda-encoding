[EN](README.md) | **TR**

# Zomato Bangalore Restoranları — Keşifsel Veri Analizi ve Özellik Mühendisliği

Zomato Bangalore Restoranları veri seti (51.717 restoran, 17 sütun) üzerinde keşifsel veri analizi ve özellik mühendisliği. Veri temizleme, eksik değer yönetimi, encoding ve restoran puanlarıyla ilişkili faktörlerin görsel analizini kapsar.

## 📊 Veri Seti

- **Kaynak:** [Zomato Bangalore Restaurants](https://www.kaggle.com/datasets/himanshupoddar/zomato-bangalore-restaurants) (Kaggle)
- **Boyut:** 51.717 satır × 17 sütun
- Zomato üzerinden Bangalore, Hindistan için scrape edilmiş restoran verileri — online sipariş, masa rezervasyonu, puanlar, oy sayısı, konum, restoran türü, mutfak türleri, yaklaşık maliyet, yorumlar ve menü öğeleri.

### Veri Seti Sütunları

| Sütun | Açıklama | Not |
|---|---|---|
| `url` | Restoranın Zomato sayfası URL'si | |
| `address` | Restoranın adresi | |
| `name` | Restoran adı | |
| `online_order` | Online sipariş imkanı olup olmadığı | `online_order_Yes` olarak encode edildi |
| `book_table` | Masa rezervasyonu imkanı olup olmadığı | `book_table_Yes` olarak encode edildi |
| `rate` | 5 üzerinden genel puan | `rate(over 5)` olarak yeniden adlandırıldı |
| `votes` | Alınan toplam oy sayısı | |
| `phone` | Restoranın telefon numarası/numaraları | `phone_first` / `phone_secondary` olarak ayrıldı |
| `location` | Restoranın bulunduğu mahalle | |
| `rest_type` | Restoran türü (örn. Casual Dining, Cafe) | |
| `dish_liked` | Müşterilerin beğendiği yemekler | Düşürüldü — %54 eksik |
| `cuisines` | Virgülle ayrılmış mutfak türleri | |
| `approx_cost(for two people)` | İki kişilik yaklaşık maliyet | |
| `reviews_list` | (puan, yorum) demetlerinden oluşan liste | |
| `menu_item` | Menü öğelerinin listesi | Düşürüldü — ~%76 boş |
| `listed_in(type)` | Hizmet türü (Delivery, Dine-out vb.) | One-hot encode edildi |
| `listed_in(city)` | İlanın kayıtlı olduğu mahalle | |

## 🎯 Proje Hedefleri

- Karmaşık, gerçek dünyadan scrape edilmiş bir veri setini temizlemek ve standardize etmek (karışık veri tipleri, tutarsız formatlar, encoding sorunları)
- Eksik değerleri toptan (blanket) bir yöntem yerine bağlama uygun stratejilerle yönetmek
- Kategorik değişkenleri sonraki modelleme için encode etmek
- Restoran özellikleri (maliyet, oy sayısı, masa rezervasyonu) ile puanlar arasındaki ilişkileri keşfetmek

## 🧹 Veri Temizleme

1. **Puan sütunu (`rate` → `rate(over 5)`)**
   - Placeholder değerler (`"NEW"`, `"-"`) `NaN` ile değiştirildi
   - `/5` son eki kaldırıldı, `float` tipine çevrildi
2. **Telefon sütunu**
   - `phone_first` ve `phone_secondary` olarak iki sütuna ayrıldı (bazı restoranlarda `\r\n` ile ayrılmış iki numara vardı)
   - Tutarlı bir format için `+` işareti ve boşluklar temizlendi
3. **Maliyet sütunu (`approx_cost(for two people)`)**
   - Binlik ayırıcılar (`,`) kaldırıldı, `float` tipine çevrildi

## 🕳 Eksik Değer Yönetimi

| Sütun | Eksik | Strateji |
|---|---|---|
| `rate(over 5)` | 10.052 | `listed_in(type)` bazında grup medyanı |
| `dish_liked` | 28.078 (%54) | Düşürüldü — güvenilir olamayacak kadar seyrek |
| `menu_item` | ~%76 boş liste (`'[]'`) | Düşürüldü |
| `location` / `cuisines` | 21 / 45 | Satırlar düşürüldü (verinin çok küçük bir kısmı) |
| `rest_type` | 227 | Mode ile doldurma (`Quick Bites`) |
| `approx_cost(for two people)` | 346 | `listed_in(type)` bazında grup medyanı |
| `phone_first` / `phone_secondary` | 1.179 / 31.661 | Olduğu gibi bırakıldı — yapısal olarak eksik (çoğu restoranda tek numara var) |

## 🔢 Encoding

- `online_order`, `book_table` → one-hot encode edildi (`drop_first=True`)
- `listed_in(type)` → one-hot encode edildi (`drop_first=True`, referans kategori: `Buffet`)

## 📈 Keşifsel Veri Analizi

### Korelasyon matrisi
![Korelasyon ısı haritası](images/zom_corr.png)

- `book_table` ve `approx_cost` en güçlü ilişkiyi gösteriyor (**0.62**) — masa rezervasyonu kabul eden restoranlar belirgin şekilde daha pahalı olma eğiliminde.
- `rate`, `votes` (0.42), `book_table` (0.41) ve `approx_cost` (0.37) ile orta seviyede korele.
- `listed_in(type)_*` dummy sütunları arasındaki negatif korelasyonlar (örn. Delivery vs. Dine-out: -0.73) one-hot encoding'in yapısal bir yan etkisi, gerçek bir ilişki değil.

### Dağılımlar
![Dağılım histogramları](images/zom_hist.png)

- `votes` ve `approx_cost` belirgin şekilde sağa çarpık (uzun kuyruklu) dağılımlar.
- `rate(over 5)` sütununda **3.7** civarında yapay bir sivrilik var — kaynağı grup medyanı ile imputation: `Delivery` ve `Dine-out` (veri setinin %84'ü) ikisinin de medyan puanı 3.7 olduğu için, binlerce doldurulmuş değer aynı noktada birikti. Metodolojik bir yan etki, organik bir örüntü değil.

### Rate vs. oy sayısı / maliyet / masa rezervasyonu
![Scatter ve boxplot grafikleri](images/zom_scatterplot_boxplot.png)

- Az oy alan restoranlarda puan varyansı geniş (1.8'den 4.9'a); çok oy alan restoranlar 4.0-4.9 aralığında toplanıyor — klasik küçük örneklem varyans etkisi.
- Masa rezervasyonu kabul eden restoranlar, kabul etmeyenlere göre belirgin şekilde daha yüksek ve daha dar bir puan dağılımına sahip (medyan ~4.2'ye karşı ~3.7).

### Maliyet vs. masa rezervasyonu
![Masa rezervasyonuna göre maliyet](images/zom_box.png)

- Masa rezervasyonu olmayan restoranlarda medyan maliyet: **~₹400-450**
- Masa rezervasyonu olan restoranlarda medyan maliyet: **~₹1.200** (~3 kat daha yüksek), iki grubun çeyrekler arası aralığı (IQR) neredeyse hiç çakışmıyor.

## 🛠 Teknoloji Yığını

- Python — pandas, numpy
- seaborn, matplotlib
- scikit-learn (planlanan: `rest_type` / `cuisines` için `MultiLabelBinarizer`)

## 📁 Repo Yapısı

```
zomato-bangalore-eda/
├── README.md
├── README.tr.md
├── requirements.txt
├── notebooks/
│   └── zomato_eda.ipynb
├── scripts/
│   └── zomato_EDA_Featuring_v1.py
└── images/
    ├── zom_corr.png
    ├── zom_hist.png
    ├── zom_box.png
    └── zom_scatterplot_boxplot.png
```

## ▶️ Nasıl Çalıştırılır

```bash
pip install -r requirements.txt
python scripts/zomato_EDA_Featuring_v1.py
```

## 👤 Yazar

**Nadi Ucar**
GitHub: [@nadiucar](https://github.com/nadiucar)
