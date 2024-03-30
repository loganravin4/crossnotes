import Link from 'next/link';
import Navbar from '../components/navbar';


function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <Navbar />
      <div className="mt-20 text-center items-center">
        <h2 className="text-2xl">Welcome to Crossnotes!</h2>
        <p>Select an option below to start your journey!</p>
        <div className="flex gap-4 mt-4">
          <Link href="/components/student" className="bg-green-500 px-4 py-2 rounded-full hover:animate-bubble">Student Mode</Link>
          <Link href="/Educator" className="bg-green-500 px-4 py-2 rounded-full hover:animate-bubble">Educator Mode</Link>
        </div>
      </div>
    </div>
  );
};

export default Home;