-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 09, 2025 at 01:32 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `1herbalclassifydb`
--

-- --------------------------------------------------------

--
-- Table structure for table `admintb`
--

CREATE TABLE `admintb` (
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admintb`
--

INSERT INTO `admintb` (`UserName`, `Password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `booktb`
--

CREATE TABLE `booktb` (
  `id` bigint(10) NOT NULL auto_increment,
  `UserName` varchar(250) NOT NULL,
  `Bookid` varchar(250) NOT NULL,
  `Qty` varchar(250) NOT NULL,
  `Amount` varchar(250) NOT NULL,
  `CardName` varchar(250) NOT NULL,
  `CardNo` varchar(250) NOT NULL,
  `CvNo` varchar(250) NOT NULL,
  `Date` date NOT NULL,
  `ProductId` varchar(250) NOT NULL,
  `Image` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `booktb`
--

INSERT INTO `booktb` (`id`, `UserName`, `Bookid`, `Qty`, `Amount`, `CardName`, `CardNo`, `CvNo`, `Date`, `ProductId`, `Image`) VALUES
(1, 'mark', 'BOOKID1', '1.00', '1000.00', 'mastercard', '1234567899874563', '159', '2025-03-26', '1', 'nil'),
(2, 'mark', 'BOOKID2', '3.00', '3000.00', 'mastercard', '1234567899874563', '157', '2025-03-26', '4', 'AG-S-006.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `carttb`
--

CREATE TABLE `carttb` (
  `id` bigint(10) NOT NULL auto_increment,
  `UserName` varchar(250) NOT NULL,
  `ProductName` varchar(250) NOT NULL,
  `ProductType` varchar(250) NOT NULL,
  `Price` varchar(250) NOT NULL,
  `Qty` decimal(18,2) NOT NULL,
  `TPrice` decimal(28,2) NOT NULL,
  `Image` varchar(500) NOT NULL,
  `Date` date NOT NULL,
  `Status` varchar(250) NOT NULL,
  `Bookid` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `Address` varchar(250) NOT NULL,
  `Astatus` varchar(250) NOT NULL,
  `ProductId` varchar(250) NOT NULL,
  `Approvestatus` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `carttb`
--

INSERT INTO `carttb` (`id`, `UserName`, `ProductName`, `ProductType`, `Price`, `Qty`, `TPrice`, `Image`, `Date`, `Status`, `Bookid`, `Mobile`, `Address`, `Astatus`, `ProductId`, `Approvestatus`) VALUES
(1, 'mark', 'Coffee', 'coffee', '1000', '1.00', '1000.00', '51Catla - Copy.jpg', '2025-03-26', '1', 'BOOKID1', '24', '9087259509', 'waiting', '1', ''),
(2, 'mark', 'Coffee2', 'coffee', '1000', '1.00', '1000.00', '17Catla.jpg', '2025-03-26', '1', 'BOOKID2', '24', '9087259509', 'waiting', '4', ''),
(3, 'mark', 'Coffee2', 'coffee', '1000', '2.00', '2000.00', '17Catla.jpg', '2025-03-26', '1', 'BOOKID2', '24', '9087259509', 'waiting', '4', 'Accepted');

-- --------------------------------------------------------

--
-- Table structure for table `enttb`
--

CREATE TABLE `enttb` (
  `Name` varchar(250) NOT NULL,
  `Gender` varchar(250) NOT NULL,
  `Age` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `Address` varchar(250) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `enttb`
--

INSERT INTO `enttb` (`Name`, `Gender`, `Age`, `Email`, `Mobile`, `Address`, `UserName`, `Password`) VALUES
('jack', 'male', '24', 'javaprojectfantasy@gmail.com', '9087259509', 'Trichy', 'jack', 'jack');

-- --------------------------------------------------------

--
-- Table structure for table `producttb`
--

CREATE TABLE `producttb` (
  `id` bigint(250) NOT NULL auto_increment,
  `ProductName` varchar(250) NOT NULL,
  `ProductType` varchar(250) NOT NULL,
  `Price` varchar(250) NOT NULL,
  `Quantity` varchar(250) NOT NULL,
  `ProductInfo` varchar(250) NOT NULL,
  `Image` varchar(250) NOT NULL,
  `size` varchar(10) NOT NULL,
  `benifits` varchar(250) NOT NULL,
  `Ename` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `producttb`
--

INSERT INTO `producttb` (`id`, `ProductName`, `ProductType`, `Price`, `Quantity`, `ProductInfo`, `Image`, `size`, `benifits`, `Ename`) VALUES
(4, 'Coffee2', 'coffee', '1000', '47', 'nil', '17Catla.jpg', 'nil', 'nil', 'jack');

-- --------------------------------------------------------

--
-- Table structure for table `regtb`
--

CREATE TABLE `regtb` (
  `Name` varchar(250) NOT NULL,
  `Gender` varchar(250) NOT NULL,
  `Age` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `Address` varchar(250) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `regtb`
--

INSERT INTO `regtb` (`Name`, `Gender`, `Age`, `Email`, `Mobile`, `Address`, `UserName`, `Password`) VALUES
('mark', 'male', '24', 'javaprojectfantasy@gmail.com', '9087259509', 'Trichy', 'mark', 'mark'),
('jack', 'male', '24', 'javaprojectfantasy@gmail.com', '9087259509', 'Trichy', 'jack', 'jack');

-- --------------------------------------------------------

--
-- Table structure for table `seedtb`
--

CREATE TABLE `seedtb` (
  `sid` bigint(250) NOT NULL auto_increment,
  `Sname` varchar(250) NOT NULL,
  `Ename` varchar(250) NOT NULL,
  `Info` varchar(250) NOT NULL,
  `Image` varchar(250) NOT NULL,
  `Status` varchar(250) NOT NULL,
  PRIMARY KEY  (`sid`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `seedtb`
--

INSERT INTO `seedtb` (`sid`, `Sname`, `Ename`, `Info`, `Image`, `Status`) VALUES
(1, 'coffee', 'jack', 'coffee', '51Catla - Copy.jpg', 'Accepted'),
(2, 'Bean', 'jack', 'Bean', '51.jpg', 'Waiting');
