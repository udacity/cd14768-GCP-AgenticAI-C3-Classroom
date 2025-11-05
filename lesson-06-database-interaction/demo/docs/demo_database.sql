-- Create the demo database
CREATE DATABASE IF NOT EXISTS demo;
USE demo;

-- Create the authors table
CREATE TABLE IF NOT EXISTS authors (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birth_year INT
);

-- Create the books table
CREATE TABLE IF NOT EXISTS books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author_id INT NOT NULL,
    publication_year INT,
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);

-- Insert sample data into authors table
INSERT INTO authors (name, birth_year) VALUES
    ('J.R.R. Tolkien', 1892),
    ('George Orwell', 1903),
    ('Jane Austen', 1775),
    ('Agatha Christie', 1890),
    ('Stephen King', 1947),
    ('C.S. Lewis', 1898),
    ('Aldous Huxley', 1894),
    ('F. Scott Fitzgerald', 1896),
    ('Mary Shelley', 1797),
    ('George Eliot', 1819),
    ('Leo Tolstoy', 1828),
    ('Mark Twain', 1835),
    ('Ernest Hemingway', 1899),
    ('Virginia Woolf', 1882),
    ('William Faulkner', 1897),
    ('John Steinbeck', 1902),
    ('J.D. Salinger', 1919),
    ('Harper Lee', 1926),
    ('Toni Morrison', 1931),
    ('Alice Walker', 1944),
    ('Maya Angelou', 1928);

-- Insert sample data into books table
INSERT INTO books (title, author_id, publication_year) VALUES
    ('The Hobbit', 1, 1937),
    ('The Lord of the Rings', 1, 1954),
    ('Nineteen Eighty-Four', 2, 1949),
    ('Animal Farm', 2, 1945),
    ('Pride and Prejudice', 3, 1813),
    ('The Mysterious Affair at Styles', 4, 1920),
    ('And Then There Were None', 4, 1939),
    ('The Shining', 5, 1977),
    ('It', 5, 1986),
    ('The Lion, the Witch and the Wardrobe', 6, 1950),
    ('Brave New World', 7, 1932),
    ('The Great Gatsby', 8, 1925),
    ('Frankenstein', 9, 1818),
    ('Middlemarch', 10, 1871),
    ('War and Peace', 11, 1869),
    ('Anna Karenina', 11, 1877),
    ('Adventures of Huckleberry Finn', 12, 1884),
    ('The Old Man and the Sea', 13, 1952),
    ('Mrs Dalloway', 14, 1925),
    ('The Sound and the Fury', 15, 1929),
    ('The Grapes of Wrath', 16, 1939),
    ('The Catcher in the Rye', 17, 1951),
    ('To Kill a Mockingbird', 18, 1960),
    ('Beloved', 19, 1987),
    ('The Color Purple', 20, 1982),
    ('I Know Why the Caged Bird Sings', 21, 1969);
