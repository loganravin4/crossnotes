import Link from "next/link";
import Navbar from "../../components/navbar";

function About(){
    return (
        <div className="flex flex-col items-center justify-center min-h-screen">
          <Navbar />
          <div className="mt-20 text-center items-center">
            <h2 className="text-2xl">We are Northeastern University Students interested in Machine Learning and Artificial Intelligence!</h2>
          </div>
        </div>
      );
}

export default About;