import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Chip,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Typography,
} from '@mui/material';

const TAG_OPTIONS = ['bookable', 'breakfast', 'parking', 'late checkout', 'adult', 'teen', 'child', 'baby'];

const UpsellProductSelector = () => {
  const [hotels, setHotels] = useState([]);
  const [selectedHotelId, setSelectedHotelId] = useState('');
  const [upsellProducts, setUpsellProducts] = useState([]);
  const [rows, setRows] = useState([]);

  const tagColors = { bookable: 'green', breakfast: 'orange',  parking: 'blue', 'late checkout': 'cyan', adult: 'purple', teen: 'pink', child: 'yellow', baby: 'brown' };

  // Fetch hotels when component mounts.
  useEffect(() => {
    fetch('http://localhost:8000/api/hotels/')
      .then((res) => res.json())
      .then((data) => {
        setHotels(data.hotels || []);
      })
      .catch((error) => console.error('Error fetching hotels:', error));
  }, []);

  // When a hotel is selected, fetch upsell products.
  useEffect(() => {
    if (selectedHotelId) {
      fetch(`http://localhost:8000/api/hotels/${selectedHotelId}/upsell-products/`)
        .then((res) => res.json())
        .then((data) => {
          setUpsellProducts(data.upsell_products || []);
          setRows([]); // Reset rows when hotel changes.
        })
        .catch((error) => console.error('Error fetching upsell products:', error));
    }
  }, [selectedHotelId]);

  const addRow = () => {
    setRows([...rows, { productId: '', tags: [] }]);
  };

  const removeRow = (index) => {
    const newRows = [...rows];
    newRows.splice(index, 1);
    setRows(newRows);
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
      setRows(newRows);
    }
  };

  const removeTag = (rowIndex, tag) => {
    const newRows = [...rows];
    newRows[rowIndex].tags = newRows[rowIndex].tags.filter((t) => t !== tag);
    setRows(newRows);
  };

  // Exclude upsell products that are already selected in other rows.
  const availableUpsellProducts = (currentRowIndex) => {
    const selectedProductIds = rows
      .filter((_, idx) => idx !== currentRowIndex)
      .map((row) => row.productId)
      .filter(Boolean);
    return upsellProducts.filter(
      (product) => !selectedProductIds.includes(product.id)
    );
  };

  return (
    <Box sx={{ p: 4 }}>
      <Typography variant="h4" gutterBottom>
        Select a Hotel
      </Typography>
      <FormControl fullWidth sx={{ mb: 4 }}>
        <InputLabel id="hotel-select-label">Hotel</InputLabel>
        <Select
          labelId="hotel-select-label"
          value={selectedHotelId}
          label="Hotel"
          onChange={(e) => setSelectedHotelId(e.target.value)}
        >
          <MenuItem value="">
            <em>None</em>
          </MenuItem>
          {hotels.map((hotel) => (
            <MenuItem key={hotel.id} value={hotel.id}>
              {hotel.name} - {hotel.city} ({hotel.pms})
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      {selectedHotelId && (
        <Box>
          <Typography variant="h5" gutterBottom>
            Upsell Products
          </Typography>
          {rows.map((row, index) => (
            <Box
              key={index}
              sx={{
                border: '1px solid #ccc',
                p: 2,
                mb: 2,
                borderRadius: 1,
              }}
            >
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                <FormControl fullWidth>
                  <InputLabel id={`upsell-select-${index}`}>
                    Upsell Product
                  </InputLabel>
                  <Select
                    labelId={`upsell-select-${index}`}
                    value={row.productId}
                    label="Upsell Product"
                    onChange={(e) => handleProductChange(index, e.target.value)}
                  >
                    <MenuItem value="">
                      <em>None</em>
                    </MenuItem>
                    {availableUpsellProducts(index).map((product) => (
                      <MenuItem key={product.id} value={product.id}>
                        {product.name} ({product.price})
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <FormControl fullWidth>
                  <InputLabel id={`tag-select-${index}`}>Tag</InputLabel>
                  <Select
                    labelId={`tag-select-${index}`}
                    value=""
                    label="Tag"
                    onChange={(e) => handleTagSelect(index, e.target.value)}
                  >
                    <MenuItem value="">
                      <em>None</em>
                    </MenuItem>
                    {TAG_OPTIONS.filter((tag) => !row.tags.includes(tag)).map(
                      (tag) => (
                        <MenuItem key={tag} value={tag}>
                          {tag}
                        </MenuItem>
                      )
                    )}
                  </Select>
                </FormControl>
                <Button
                  variant="outlined"
                  color="error"
                  onClick={() => removeRow(index)}
                  sx={{ px: 3 }}
                >
                  Remove
                </Button>
              </Box>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {row.tags.map((tag, idx) => (
                  <Chip
                    key={idx}
                    label={tag}
                    onDelete={() => removeTag(index, tag)}
                  />
                ))}
              </Box>
            </Box>
          ))}
          <Button variant="contained" onClick={addRow}>
            Add Upsell Product Row
          </Button>
        </Box>
      )}
    </Box>
  );
};

export default UpsellProductSelector;
