'use client'
import { useEffect, useState } from 'react';
import Link from "next/link";
import Navbar from "../../components/navbar";

function Student(){
  const [crossword, setCrossword] = useState(null);
  const [selectedFile, setSelectedFile] = useState<File | undefined>();

  const generateCrossword = async (pdfFile: File) => {
    const formData = new FormData();
    formData.append('pdf', pdfFile);

    const response = await fetch('http://127.0.0.1:5000/generate_crossword', {
      method: 'POST',
      body: formData,
    });
    
    if (!response.ok) {
      console.log('Network response was not ok');
      //throw new Error('Network response was not ok');
    }

    const crossword = await response.json();
    return crossword;
  };

  useEffect(() => {
    if (selectedFile) {
      generateCrossword(selectedFile).then(setCrossword);
    }
  }, [selectedFile]);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setSelectedFile(event.target.files[0]);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <Navbar />
      <div className="mt-20 text-center items-center">
        <h2 className="text-2xl">Welcome Student!</h2>
        <input type="file" accept=".pdf" onChange={handleFileUpload} />
        {crossword && <p>{JSON.stringify(crossword)}</p>}
      </div>
    </div>
  );
}

export default Student;
