package com.lab2.backend.service;

import com.lab2.backend.model.CatalogItem;
import org.springframework.stereotype.Service;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

@Service
public class CatalogService {
    // CSV file name (searches common locations). The service will look for
    // a `catalog.csv` file in the current working directory (where the JVM
    // was started) and then in the parent directory. If not present it will
    // create a new file with a header in the working directory.
    private static final String CSV_FILENAME = "catalog.csv";
    private static final String CSV_DELIMITER = ",";

    private java.nio.file.Path resolveCsvPath() throws java.io.IOException {
        java.nio.file.Path cwd = java.nio.file.Paths.get("").toAbsolutePath();
        java.nio.file.Path p1 = cwd.resolve(CSV_FILENAME);
        if (java.nio.file.Files.exists(p1)) {
            return p1;
        }
        // try parent (useful when running from repo root and backend is in subfolder)
        java.nio.file.Path parent = cwd.getParent();
        if (parent != null) {
            java.nio.file.Path p2 = parent.resolve(CSV_FILENAME);
            if (java.nio.file.Files.exists(p2)) {
                return p2;
            }
        }
        // try backend directory (in case jar runs with repo root as cwd)
        java.nio.file.Path backendPath = cwd.resolve("backend").resolve(CSV_FILENAME);
        if (java.nio.file.Files.exists(backendPath)) {
            return backendPath;
        }
        // not found: default to creating/using p1 (cwd/catalog.csv)
        // ensure parent dirs exist and create file with header
        java.nio.file.Files.createDirectories(p1.getParent() == null ? java.nio.file.Paths.get(".") : p1.getParent());
        if (!java.nio.file.Files.exists(p1)) {
            try (java.io.PrintWriter pw = new java.io.PrintWriter(java.nio.file.Files.newBufferedWriter(p1))) {
                pw.println("ID,Name,Description");
            }
        }
        return p1;
    }

    /**
     * Milestone 1: Read all items from CSV file and parse into list of objects
     */
    public List<CatalogItem> getAllItems() {
        List<CatalogItem> items = new ArrayList<>();
        java.nio.file.Path csvPath;
        try {
            csvPath = resolveCsvPath();
        } catch (java.io.IOException e) {
            System.err.println("Error resolving CSV path: " + e.getMessage());
            e.printStackTrace();
            return items;
        }
        System.out.println("Reading CSV from: " + csvPath.toAbsolutePath());

        try (BufferedReader br = java.nio.file.Files.newBufferedReader(csvPath)) {
            String line;
            boolean isHeader = true;
            while ((line = br.readLine()) != null) {
                if (isHeader) {
                    isHeader = false;
                    continue; // Skip header row
                }
                String[] values = line.split(CSV_DELIMITER, -1);
                if (values.length >= 3) {
                    int id = Integer.parseInt(values[0].trim());
                    String name = values[1].trim();
                    String description = values[2].trim();
                    items.add(new CatalogItem(id, name, description));
                }
            }
            System.out.println("Loaded " + items.size() + " items from CSV");
        } catch (IOException e) {
            System.err.println("Error reading CSV: " + e.getMessage());
            e.printStackTrace();
        }
        return items;
    }

    /**
     * Get a single item by ID
     */
    public CatalogItem getItemById(int id) {
        return getAllItems().stream()
                .filter(item -> item.getId() == id)
                .findFirst()
                .orElse(null);
    }

    /**
     * Milestone 3: Add a new item with auto-generated ID
     */
    public CatalogItem addItem(CatalogItem newItem) {
        List<CatalogItem> items = getAllItems();
        
        // Generate new ID (max + 1)
        int maxId = items.stream()
                .mapToInt(CatalogItem::getId)
                .max()
                .orElse(0);
        newItem.setId(maxId + 1);
        
        items.add(newItem);
        saveAllItems(items);
        System.out.println("Added new item with ID: " + newItem.getId());
        return newItem;
    }

    /**
     * Milestone 3: Update an existing item
     */
    public CatalogItem updateItem(int id, CatalogItem updatedItem) {
        List<CatalogItem> items = getAllItems();
        for (int i = 0; i < items.size(); i++) {
            if (items.get(i).getId() == id) {
                updatedItem.setId(id);
                items.set(i, updatedItem);
                saveAllItems(items);
                System.out.println("Updated item ID: " + id);
                return updatedItem;
            }
        }
        return null;
    }

    /**
     * Delete an item by ID
     */
    public boolean deleteItem(int id) {
        List<CatalogItem> items = getAllItems();
        boolean removed = items.removeIf(item -> item.getId() == id);
        if (removed) {
            saveAllItems(items);
            System.out.println("Deleted item ID: " + id);
        }
        return removed;
    }

    /**
     * Milestone 4: Save all items back to CSV file
     */
    private void saveAllItems(List<CatalogItem> items) {
        try {
            java.nio.file.Path csvPath = resolveCsvPath();
            try (java.io.PrintWriter pw = new java.io.PrintWriter(java.nio.file.Files.newBufferedWriter(csvPath))) {
                pw.println("ID,Name,Description");
                for (CatalogItem item : items) {
                    pw.println(item.getId() + CSV_DELIMITER +
                              item.getName() + CSV_DELIMITER +
                              item.getDescription());
                }
            }
            System.out.println("Saved " + items.size() + " items to CSV at " + resolveCsvPath());
        } catch (IOException e) {
            System.err.println("Error saving CSV: " + e.getMessage());
            e.printStackTrace();
        }
    }

    /**
     * Milestone 3: Validate item input (non-empty fields)
     */
    public boolean validateItem(CatalogItem item) {
        return item.getName() != null && !item.getName().trim().isEmpty() &&
               item.getDescription() != null && !item.getDescription().trim().isEmpty();
    }
    
}
