// UpsellProductSelector.js
import React, { useState, useEffect } from 'react';

const TAG_OPTIONS = ['bookable', 'breakfast', 'parking', 'late checkout'];

const UpsellProductSelector = () => {
  const [hotels, setHotels] = useState([]);
  const [selectedHotelId, setSelectedHotelId] = useState('');
  const [upsellProducts, setUpsellProducts] = useState([]);
  const [rows, setRows] = useState([]);

  // Fetch hotels on mount
  useEffect(() => {
    fetch('/api/hotels/')
      .then((res) => res.json())
      .then((data) => {
        setHotels(data.hotels || []);
      })
      .catch((error) => console.error('Error fetching hotels:', error));
  }, []);

  // Fetch upsell products when a hotel is selected
  useEffect(() => {
    if (selectedHotelId) {
      fetch(`/api/hotels/${selectedHotelId}/upsell-products/`)
        .then((res) => res.json())
        .then((data) => {
          setUpsellProducts(data.upsell_products || []);
          // Reset rows if hotel changes
          setRows([]);
        })
        .catch((error) => console.error('Error fetching upsell products:', error));
    }
  }, [selectedHotelId]);

  const addRow = () => {
    setRows([...rows, { productId: '', tags: [] }]);
  };

  const removeRow = (index) => {
    setRows(rows.filter((_, i) => i !== index));
  };

  const handleProductChange = (index, productId) => {
    const newRows = [...rows];
    newRows[index].productId = productId;
    setRows(newRows);
  };

  const handleTagSelect = (rowIndex, tag) => {
    const newRows = [...rows];
    if (!newRows[rowIndex].tags.includes(tag)) {
      newRows[rowIndex].tags.push(tag);
    }
    setRows(newRows);
  };

  const removeTag = (rowIndex, tag) => {
    const newRows = [...rows];
    newRows[rowIndex].tags = newRows[rowIndex].tags.filter(t => t !== tag);
    setRows(newRows);
  };

  // Returns available upsell products for a given row (excluding those already selected in other rows)
  const availableUpsellProducts = (currentRowIndex) => {
    const selectedProductIds = rows
      .filter((_, idx) => idx !== currentRowIndex)
      .map(row => row.productId)
      .filter(Boolean);
    return upsellProducts.filter(product => !selectedProductIds.includes(product.id));
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Select a Hotel</h2>
      <select
        value={selectedHotelId}
        onChange={(e) => setSelectedHotelId(e.target.value)}
      >
        <option value="">-- Select a Hotel --</option>
        {hotels.map((hotel) => (
          <option key={hotel.id} value={hotel.id}>
            {hotel.name} - {hotel.city} ({hotel.pms})
          </option>
        ))}
      </select>

      {selectedHotelId && (
        <div>
          <h2>Upsell Products</h2>
          {rows.map((row, index) => (
            <div key={index} style={{ border: '1px solid #ccc', padding: '10px', marginBottom: '10px' }}>
              <div style={{ display: 'flex', alignItems: 'center' }}>
                <div style={{ flex: 1, marginRight: '10px' }}>
                  <label>Upsell Product: </label>
                  <select
                    value={row.productId}
                    onChange={(e) => handleProductChange(index, e.target.value)}
                  >
                    <option value="">-- Select a Product --</option>
                    {availableUpsellProducts(index).map((product) => (
                      <option key={product.id} value={product.id}>
                        {product.name} ({product.price})
                      </option>
                    ))}
                  </select>
                </div>
                <div style={{ flex: 1, marginRight: '10px' }}>
                  <label>Tags: </label>
                  <select
                    onChange={(e) => {
                      const tag = e.target.value;
                      if (tag) {
                        handleTagSelect(index, tag);
                      }
                    }}
                  >
                    <option value="">-- Select a Tag --</option>
                    {TAG_OPTIONS.filter((tag) => !row.tags.includes(tag)).map((tag) => (
                      <option key={tag} value={tag}>
                        {tag}
                      </option>
                    ))}
                  </select>
                </div>
                <button onClick={() => removeRow(index)}>Remove Row</button>
              </div>
              <div style={{ marginTop: '10px' }}>
                {row.tags.map((tag, idx) => (
                  <span key={idx} style={{ marginRight: '5px', padding: '4px', background: '#e0e0e0', borderRadius: '4px' }}>
                    {tag} <button onClick={() => removeTag(index, tag)}>x</button>
                  </span>
                ))}
              </div>
            </div>
          ))}
          <button onClick={addRow}>Add Upsell Product Row</button>
        </div>
      )}
    </div>
  );
};

export default UpsellProductSelector;
