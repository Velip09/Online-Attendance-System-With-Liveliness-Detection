-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 17, 2022 at 05:46 PM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `database`
--

-- --------------------------------------------------------

--
-- Table structure for table `faculty`
--

CREATE TABLE `faculty` (
  `Sno` int(11) NOT NULL,
  `Fname` varchar(15) NOT NULL,
  `Lname` varchar(15) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `PNo` int(11) NOT NULL,
  `Department` varchar(50) NOT NULL,
  `Gender` varchar(50) NOT NULL,
  `Password` varchar(50) NOT NULL,
  `Cpassword` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `faculty`
--

INSERT INTO `faculty` (`Sno`, `Fname`, `Lname`, `Email`, `PNo`, `Department`, `Gender`, `Password`, `Cpassword`) VALUES
(1, 'GANGESH', 'VELIP', 'velip09@gmail.com', 2147483647, '1', '2', '123', '123'),
(2, 'Shiva', 'Sawant', 'shiva@gmail.com', 12345678, 'ETC', 'Male', '123', '123');

-- --------------------------------------------------------

--
-- Table structure for table `notice`
--

CREATE TABLE `notice` (
  `Sno` int(11) NOT NULL,
  `message` varchar(5000) NOT NULL,
  `Date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `notice`
--

INSERT INTO `notice` (`Sno`, `message`, `Date`) VALUES
(1, '   Hello', '2022-06-17 00:00:00'),
(2, '   Hello', '2022-06-17 00:00:00'),
(3, '            hello', '2022-06-17 11:02:43');

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student` (
  `Sno.` int(11) NOT NULL,
  `Fname` varchar(50) NOT NULL,
  `Lname` varchar(50) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Pno` int(11) NOT NULL,
  `Eno` int(11) NOT NULL,
  `Rno` varchar(50) NOT NULL,
  `Bdate` date NOT NULL,
  `Gender` varchar(50) NOT NULL,
  `Department` varchar(50) NOT NULL,
  `Semester` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `Cpassword` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`Sno.`, `Fname`, `Lname`, `Email`, `Pno`, `Eno`, `Rno`, `Bdate`, `Gender`, `Department`, `Semester`, `password`, `Cpassword`) VALUES
(1, 'GANGESH', 'VELIP', 'velip09@gmail.com', 2147483647, 12345, '123', '2022-06-15', 'Male', 'ETC', 'IV', '1234', '1234');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `faculty`
--
ALTER TABLE `faculty`
  ADD PRIMARY KEY (`Sno`);

--
-- Indexes for table `notice`
--
ALTER TABLE `notice`
  ADD PRIMARY KEY (`Sno`);

--
-- Indexes for table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`Sno.`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `faculty`
--
ALTER TABLE `faculty`
  MODIFY `Sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `notice`
--
ALTER TABLE `notice`
  MODIFY `Sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `student`
--
ALTER TABLE `student`
  MODIFY `Sno.` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
