import Link from 'next/link';

function Navbar() {
  return (
    <div className="grid grid-cols-3 items-center p-4 bg-blue-500 text-white w-full fixed top-0">
      <div className="flex gap-4 justify-start">
        <Link href="/" className="bg-green-500 px-4 py-2 rounded-none">Home</Link>
        <Link href="/components/about" className="bg-green-500 px-4 py-2 rounded-none">About Us</Link>
      </div>
      <h1 className="text-2xl text-center">Crossnotes</h1>
      <div className="flex gap-4 justify-end">
        <Link href="/components/login" className="bg-green-500 px-4 py-2 rounded-full">Login</Link>
        <Link href="/components/signup" className="bg-green-500 px-4 py-2 rounded-full">Sign Up</Link>
      </div>
    </div>
  );
};

export default Navbar;