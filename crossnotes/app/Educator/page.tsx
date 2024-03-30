import Link from 'next/link';
import Navbar from '../../components/navbar';

function Educator() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <Navbar />
      <div className="mt-20 text-center items-center">
        <h2 className="text-2xl">Welcome Educator!</h2>
      </div>
    </div>
  );
};

export default Educator;