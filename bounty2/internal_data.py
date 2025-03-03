DATA = {
    "Iberian Orchard Exports": {
      "documentation_metadata": {
        "Document ID": "DOC-1001",
        "Exporter ID": "EX001",
        "Document Type": "Bill of Lading",
        "Format": "Electronic",
        "Date Issued": "2025-05-09",
        "Validity Period": "1 Year",
        "Departure Port": "Valencia Port",
        "Linked Shipment ID": "S-1001",
        "Linked Traceability Record IDs": ["TR-0001", "TR-0002"],
        "Status": "Approved",
        "Comments": "All documentation verified; complete record."
      },
      "shipments": {
        "Shipment ID": "S-1001",
        "Exporter ID": "EX001",
        "Country of Origin": "Spain",
        "Destination Country": "United States",
        "Product Type": "Fruit",
        "Product Description": "Fresh Apples",
        "HS Code": 808.1,
        "Quantity": "1000 kg",
        "Export Date": "2025-05-10",
        "Departure Port": "Valencia Port",
        "Arrival Port": "Los Angeles",
        "Shipping Modality": "Ocean Freight",
        "Carrier": "MSC",
        "Compliance Status": "Compliant",
        "Linked Traceability Record IDs": ["TR-0001", "TR-0002"]
      },
      "traceability_data": {
        "TR-0001": {
          "Exporter ID": "EX001",
          "Food Product": "Apples",
          "CTE Type": "Production",
          "KDE Details": "Orchard Harvest; Quality: A",
          "Timestamp": "2025-05-01 08:00",
          "Compliance Flag": "Pass",
          "Temp (°C)": 20,
          "Humidity (%)": 55,
          "Location (Name & Coords)": "Valencia Orchard (39.4702° N, 0.3768° W)",
          "Lot Number": "L-AP-001",
          "Batch Number": "B001",
          "Supplier ID": "SUP-OR-001",
          "Comments": "Harvested under optimal conditions."
        },
        "TR-0002": {
          "Exporter ID": "EX001",
          "Food Product": "Apples",
          "CTE Type": "Packaging",
          "KDE Details": "Packed in Crates; Weight: 10 kg/pack",
          "Timestamp": "2025-05-01 10:00",
          "Compliance Flag": "Pass",
          "Temp (°C)": 18,
          "Humidity (%)": 50,
          "Location (Name & Coords)": "Iberian Packing Facility (39.4825° N, 0.3817° W)",
          "Lot Number": "L-AP-001",
          "Batch Number": "B001",
          "Supplier ID": "SUP-OR-001",
          "Comments": "Packaging verified; seals intact."
        }
      }
    },
    "BellaCarota Organics": {
      "documentation_metadata": {
        "Document ID": "DOC-1002",
        "Exporter ID": "EX002",
        "Document Type": "Export License",
        "Format": "Paper",
        "Date Issued": "2025-05-11",
        "Validity Period": "6 Months",
        "Departure Port": "Port of Genoa",
        "Linked Shipment ID": "S-1002",
        "Linked Traceability Record IDs": ["TR-0003", "TR-0012"],
        "Status": "Pending Review",
        "Comments": "Some documentation incomplete; needs update."
      },
      "shipments": {
        "Shipment ID": "S-1002",
        "Exporter ID": "EX002",
        "Country of Origin": "Italy",
        "Destination Country": "United States",
        "Product Type": "Vegetable",
        "Product Description": "Organic Carrots",
        "HS Code": 707.1,
        "Quantity": "500 kg",
        "Export Date": "2025-05-12",
        "Departure Port": "Port of Genoa",
        "Arrival Port": "New York",
        "Shipping Modality": "Air Freight",
        "Carrier": "Alitalia Cargo",
        "Compliance Status": "Non-Compliant",
        "Linked Traceability Record IDs": ["TR-0003", "TR-0012"]
      },
      "traceability_data": {
        "TR-0003": {
          "Exporter ID": "EX002",
          "Food Product": "Carrots",
          "CTE Type": "Production",
          "KDE Details": "Field Harvest; Quality Score: 92",
          "Timestamp": "2025-05-03 09:00",
          "Compliance Flag": "Fail",
          "Temp (°C)": 22,
          "Humidity (%)": 60,
          "Location (Name & Coords)": "Tuscany Farm (43.7711° N, 11.2486° E)",
          "Lot Number": "L-CR-002",
          "Batch Number": "B002",
          "Supplier ID": "SUP-FA-002",
          "Comments": "Inconsistent size observed; batch details missing."
        },
        "TR-0012": {
          "Exporter ID": "EX002",
          "Food Product": "Carrots",
          "CTE Type": "N/A",
          "KDE Details": "No data in this sample; placeholder for demonstration.",
          "Timestamp": "N/A",
          "Compliance Flag": "N/A",
          "Temp (°C)": 0,
          "Humidity (%)": 0,
          "Location (Name & Coords)": "N/A",
          "Lot Number": "N/A",
          "Batch Number": "N/A",
          "Supplier ID": "N/A",
          "Comments": "N/A"
        }
      }
    },
    "Le Bœuf Exquis": {
      "documentation_metadata": {
        "Document ID": "DOC-1003",
        "Exporter ID": "EX003",
        "Document Type": "Certificate of Origin",
        "Format": "Electronic",
        "Date Issued": "2025-05-13",
        "Validity Period": "1 Year",
        "Departure Port": "Le Havre",
        "Linked Shipment ID": "S-1003",
        "Linked Traceability Record IDs": ["TR-0004", "TR-0013"],
        "Status": "Approved",
        "Comments": "Verified against traceability records."
      },
      "shipments": {
        "Shipment ID": "S-1003",
        "Exporter ID": "EX003",
        "Country of Origin": "France",
        "Destination Country": "United States",
        "Product Type": "Meat",
        "Product Description": "Premium Beef Cuts",
        "HS Code": 202.1,
        "Quantity": "300 kg",
        "Export Date": "2025-05-15",
        "Departure Port": "Le Havre",
        "Arrival Port": "Houston",
        "Shipping Modality": "Ocean Freight",
        "Carrier": "CMA CGM",
        "Compliance Status": "Compliant",
        "Linked Traceability Record IDs": ["TR-0004", "TR-0013"]
      },
      "traceability_data": {
        "TR-0004": {
          "Exporter ID": "EX003",
          "Food Product": "Beef",
          "CTE Type": "Production",
          "KDE Details": "Initial Slaughter; Temp: 4°C; Quality: A",
          "Timestamp": "2025-05-05 07:30",
          "Compliance Flag": "Pass",
          "Temp (°C)": 4,
          "Humidity (%)": 40,
          "Location (Name & Coords)": "Normandy Processing Plant (49.1829° N, 0.3700° W)",
          "Lot Number": "L-BF-003",
          "Batch Number": "B003",
          "Supplier ID": "SUP-HP-003",
          "Comments": "All parameters within range."
        },
        "TR-0013": {
          "Exporter ID": "EX003",
          "Food Product": "Beef",
          "CTE Type": "N/A",
          "KDE Details": "No data in this sample; placeholder for demonstration.",
          "Timestamp": "N/A",
          "Compliance Flag": "N/A",
          "Temp (°C)": 0,
          "Humidity (%)": 0,
          "Location (Name & Coords)": "N/A",
          "Lot Number": "N/A",
          "Batch Number": "N/A",
          "Supplier ID": "N/A",
          "Comments": "N/A"
        }
      }
    },
    "AlpenKäse Delights": {
      "documentation_metadata": {
        "Document ID": "DOC-1004",
        "Exporter ID": "EX004",
        "Document Type": "Bill of Lading",
        "Format": "Electronic",
        "Date Issued": "2025-05-15",
        "Validity Period": "1 Year",
        "Departure Port": "Hamburg",
        "Linked Shipment ID": "S-1004",
        "Linked Traceability Record IDs": ["TR-0005", "TR-0014"],
        "Status": "Approved",
        "Comments": "Documentation meets all requirements."
      },
      "shipments": {
        "Shipment ID": "S-1004",
        "Exporter ID": "EX004",
        "Country of Origin": "Germany",
        "Destination Country": "United States",
        "Product Type": "Dairy",
        "Product Description": "Artisanal Cheese",
        "HS Code": 406.1,
        "Quantity": "200 kg",
        "Export Date": "2025-06-01",
        "Departure Port": "Hamburg",
        "Arrival Port": "Chicago",
        "Shipping Modality": "Air Freight",
        "Carrier": "Lufthansa Cargo",
        "Compliance Status": "Compliant",
        "Linked Traceability Record IDs": ["TR-0005", "TR-0014"]
      },
      "traceability_data": {
        "TR-0005": {
          "Exporter ID": "EX004",
          "Food Product": "Cheese",
          "CTE Type": "Aging",
          "KDE Details": "Cheddar; Aged 60 days; pH: 5.2",
          "Timestamp": "2025-05-07 11:00",
          "Compliance Flag": "Pass",
          "Temp (°C)": 12,
          "Humidity (%)": 75,
          "Location (Name & Coords)": "Bavarian Aging Facility (48.1351° N, 11.5820° E)",
          "Lot Number": "L-CH-004",
          "Batch Number": "B004",
          "Supplier ID": "SUP-DA-004",
          "Comments": "Aging process on schedule."
        },
        "TR-0014": {
          "Exporter ID": "EX004",
          "Food Product": "Cheese",
          "CTE Type": "N/A",
          "KDE Details": "No data in this sample; placeholder for demonstration.",
          "Timestamp": "N/A",
          "Compliance Flag": "N/A",
          "Temp (°C)": 0,
          "Humidity (%)": 0,
          "Location (Name & Coords)": "N/A",
          "Lot Number": "N/A",
          "Batch Number": "N/A",
          "Supplier ID": "N/A",
          "Comments": "N/A"
        }
      }
    },
    "Nordic Salmon Select": {
      "documentation_metadata": {
        "Document ID": "DOC-1005",
        "Exporter ID": "EX005",
        "Document Type": "Health Certificate",
        "Format": "Paper",
        "Date Issued": "2025-05-17",
        "Validity Period": "6 Months",
        "Departure Port": "Oslo",
        "Linked Shipment ID": "S-1005",
        "Linked Traceability Record IDs": ["TR-0006", "TR-0015"],
        "Status": "Pending Review",
        "Comments": "Temperature fluctuations flagged in records."
      },
      "shipments": {
        "Shipment ID": "S-1005",
        "Exporter ID": "EX005",
        "Country of Origin": "Norway",
        "Destination Country": "United States",
        "Product Type": "Seafood",
        "Product Description": "Wild Caught Salmon",
        "HS Code": 303.2,
        "Quantity": "400 kg",
        "Export Date": "2025-06-05",
        "Departure Port": "Oslo",
        "Arrival Port": "Seattle",
        "Shipping Modality": "Air Freight",
        "Carrier": "Norwegian Air Shuttle Cargo",
        "Compliance Status": "Non-Compliant",
        "Linked Traceability Record IDs": ["TR-0006", "TR-0015"]
      },
      "traceability_data": {
        "TR-0006": {
          "Exporter ID": "EX005",
          "Food Product": "Salmon",
          "CTE Type": "Processing",
          "KDE Details": "Filleting completed; Avg. Weight: 500g",
          "Timestamp": "2025-05-09 12:00",
          "Compliance Flag": "Fail",
          "Temp (°C)": 2,
          "Humidity (%)": 80,
          "Location (Name & Coords)": "Oslo Seafood Plant (59.9139° N, 10.7522° E)",
          "Lot Number": "L-SA-005",
          "Batch Number": "B005",
          "Supplier ID": "SUP-SE-005",
          "Comments": "Temperature fluctuations detected."
        },
        "TR-0015": {
          "Exporter ID": "EX005",
          "Food Product": "Salmon",
          "CTE Type": "N/A",
          "KDE Details": "No data in this sample; placeholder for demonstration.",
          "Timestamp": "N/A",
          "Compliance Flag": "N/A",
          "Temp (°C)": 0,
          "Humidity (%)": 0,
          "Location (Name & Coords)": "N/A",
          "Lot Number": "N/A",
          "Batch Number": "N/A",
          "Supplier ID": "N/A",
          "Comments": "N/A"
        }
      }
    },
    "Moroccan Sun Citrus": {
      "documentation_metadata": {
        "Document ID": "DOC-1006",
        "Exporter ID": "EX006",
        "Document Type": "Bill of Lading",
        "Format": "Electronic",
        "Date Issued": "2025-05-19",
        "Validity Period": "1 Year",
        "Departure Port": "Casablanca",
        "Linked Shipment ID": "S-1006",
        "Linked Traceability Record IDs": ["TR-0007"],
        "Status": "Approved",
        "Comments": "All data verified and compliant."
      },
      "shipments": {
        "Shipment ID": "S-1006",
        "Exporter ID": "EX006",
        "Country of Origin": "Morocco",
        "Destination Country": "United States",
        "Product Type": "Fruit",
        "Product Description": "Citrus Mix",
        "HS Code": 809.4,
        "Quantity": "750 kg",
        "Export Date": "2025-06-10",
        "Departure Port": "Casablanca",
        "Arrival Port": "Miami",
        "Shipping Modality": "Ocean Freight",
        "Carrier": "Maersk",
        "Compliance Status": "Compliant",
        "Linked Traceability Record IDs": ["TR-0007"]
      },
      "traceability_data": {
        "TR-0007": {
          "Exporter ID": "EX006",
          "Food Product": "Citrus",
          "CTE Type": "Production",
          "KDE Details": "Hand-picked; Average size: Medium",
          "Timestamp": "2025-05-11 08:30",
          "Compliance Flag": "Pass",
          "Temp (°C)": 24,
          "Humidity (%)": 45,
          "Location (Name & Coords)": "Marrakech Orchard (31.6295° N, 8.0083° W)",
          "Lot Number": "L-CT-006",
          "Batch Number": "B006",
          "Supplier ID": "SUP-OR-006",
          "Comments": "Consistent quality observed."
        }
      }
    },
    "Anatolian Harvest Organics": {
      "documentation_metadata": {
        "Document ID": "DOC-1007",
        "Exporter ID": "EX007",
        "Document Type": "Export License",
        "Format": "Electronic",
        "Date Issued": "2025-05-21",
        "Validity Period": "6 Months",
        "Departure Port": "Istanbul",
        "Linked Shipment ID": "S-1007",
        "Linked Traceability Record IDs": ["TR-0008"],
        "Status": "Approved",
        "Comments": "Compliance confirmed; documentation complete."
      },
      "shipments": {
        "Shipment ID": "S-1007",
        "Exporter ID": "EX007",
        "Country of Origin": "Turkey",
        "Destination Country": "United States",
        "Product Type": "Vegetable",
        "Product Description": "Organic Tomatoes",
        "HS Code": 702.0,
        "Quantity": "600 kg",
        "Export Date": "2025-06-15",
        "Departure Port": "Istanbul",
        "Arrival Port": "Boston",
        "Shipping Modality": "Air Freight",
        "Carrier": "Turkish Airlines Cargo",
        "Compliance Status": "Compliant",
        "Linked Traceability Record IDs": ["TR-0008"]
      },
      "traceability_data": {
        "TR-0008": {
          "Exporter ID": "EX007",
          "Food Product": "Tomatoes",
          "CTE Type": "Processing",
          "KDE Details": "Washed & Sorted; Quality Grade: A",
          "Timestamp": "2025-05-13 10:45",
          "Compliance Flag": "Pass",
          "Temp (°C)": 21,
          "Humidity (%)": 50,
          "Location (Name & Coords)": "Istanbul Processing Center (41.0082° N, 28.9784° E)",
          "Lot Number": "L-TM-007",
          "Batch Number": "B007",
          "Supplier ID": "SUP-AG-007",
          "Comments": "Standard processing completed."
        }
      }
    },
    "Frango Fino Brazil": {
      "documentation_metadata": {
        "Document ID": "DOC-1008",
        "Exporter ID": "EX008",
        "Document Type": "Certificate of Origin",
        "Format": "Paper",
        "Date Issued": "2025-05-23",
        "Validity Period": "1 Year",
        "Departure Port": "Santos",
        "Linked Shipment ID": "S-1008",
        "Linked Traceability Record IDs": ["TR-0009"],
        "Status": "Pending Review",
        "Comments": "Packaging issues noted; further review needed."
      },
      "shipments": {
        "Shipment ID": "S-1008",
        "Exporter ID": "EX008",
        "Country of Origin": "Brazil",
        "Destination Country": "United States",
        "Product Type": "Meat",
        "Product Description": "Chicken Breasts",
        "HS Code": 207.14,
        "Quantity": "800 kg",
        "Export Date": "2025-06-20",
        "Departure Port": "Santos",
        "Arrival Port": "New Orleans",
        "Shipping Modality": "Ocean Freight",
        "Carrier": "Hapag-Lloyd",
        "Compliance Status": "Non-Compliant",
        "Linked Traceability Record IDs": ["TR-0009"]
      },
      "traceability_data": {
        "TR-0009": {
          "Exporter ID": "EX008",
          "Food Product": "Chicken",
          "CTE Type": "Packaging",
          "KDE Details": "Vacuum Sealed; Weight: 1.2 kg/pack",
          "Timestamp": "2025-05-15 14:00",
          "Compliance Flag": "Fail",
          "Temp (°C)": 3,
          "Humidity (%)": 65,
          "Location (Name & Coords)": "São Paulo Facility (23.5505° S, 46.6333° W)",
          "Lot Number": "L-CH-008",
          "Batch Number": "B008",
          "Supplier ID": "SUP-CH-008",
          "Comments": "Seal integrity issues; re-check required."
        }
      }
    },
    "Nile Artisan Breads": {
      "documentation_metadata": {
        "Document ID": "DOC-1009",
        "Exporter ID": "EX009",
        "Document Type": "Bill of Lading",
        "Format": "Electronic",
        "Date Issued": "2025-05-25",
        "Validity Period": "1 Year",
        "Departure Port": "Alexandria",
        "Linked Shipment ID": "S-1009",
        "Linked Traceability Record IDs": ["TR-0010"],
        "Status": "Approved",
        "Comments": "All documentation verified and compliant."
      },
      "shipments": {
        "Shipment ID": "S-1009",
        "Exporter ID": "EX009",
        "Country of Origin": "Egypt",
        "Destination Country": "United States",
        "Product Type": "Bakery",
        "Product Description": "Artisan Breads",
        "HS Code": 1905.9,
        "Quantity": "350 kg",
        "Export Date": "2025-06-25",
        "Departure Port": "Alexandria",
        "Arrival Port": "San Francisco",
        "Shipping Modality": "Air Freight",
        "Carrier": "EgyptAir Cargo",
        "Compliance Status": "Compliant",
        "Linked Traceability Record IDs": ["TR-0010"]
      },
      "traceability_data": {
        "TR-0010": {
          "Exporter ID": "EX009",
          "Food Product": "Breads",
          "CTE Type": "Production",
          "KDE Details": "Dough Mixed; Consistency: Optimal",
          "Timestamp": "2025-05-17 09:15",
          "Compliance Flag": "Pass",
          "Temp (°C)": 25,
          "Humidity (%)": 55,
          "Location (Name & Coords)": "Cairo Bakery (30.0444° N, 31.2357° E)",
          "Lot Number": "L-BR-009",
          "Batch Number": "B009",
          "Supplier ID": "SUP-BA-009",
          "Comments": "Process within control limits."
        }
      }
    },
    "Belgian Velvet Chocolates": {
      "documentation_metadata": {
        "Document ID": "DOC-1010",
        "Exporter ID": "EX010",
        "Document Type": "Health Certificate",
        "Format": "Electronic",
        "Date Issued": "2025-05-27",
        "Validity Period": "6 Months",
        "Departure Port": "Antwerp",
        "Linked Shipment ID": "S-1010",
        "Linked Traceability Record IDs": ["TR-0011"],
        "Status": "Approved",
        "Comments": "Verified; meets all U.S. FDA requirements."
      },
      "shipments": {
        "Shipment ID": "S-1010",
        "Exporter ID": "EX010",
        "Country of Origin": "Belgium",
        "Destination Country": "United States",
        "Product Type": "Confectionery",
        "Product Description": "Gourmet Chocolates",
        "HS Code": 1806.9,
        "Quantity": "250 kg",
        "Export Date": "2025-07-01",
        "Departure Port": "Antwerp",
        "Arrival Port": "Dallas",
        "Shipping Modality": "Air Freight",
        "Carrier": "Belgian World Cargo",
        "Compliance Status": "Compliant",
        "Linked Traceability Record IDs": ["TR-0011"]
      },
      "traceability_data": {
        "TR-0011": {
          "Exporter ID": "EX010",
          "Food Product": "Chocolates",
          "CTE Type": "Packaging",
          "KDE Details": "Boxed; Temp maintained; Seal verified",
          "Timestamp": "2025-05-19 16:20",
          "Compliance Flag": "Pass",
          "Temp (°C)": 18,
          "Humidity (%)": 40,
          "Location (Name & Coords)": "Brussels Confectionery Center (50.8503° N, 4.3517° E)",
          "Lot Number": "L-CHOC-010",
          "Batch Number": "B010",
          "Supplier ID": "SUP-CO-010",
          "Comments": "Packaging process successful."
        }
      }
    }
  }
  