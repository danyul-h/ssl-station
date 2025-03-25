"use client"
import Image from "next/image";
import {motion} from "motion/react";
import {Canvas, useFrame} from "@react-three/fiber"
import { useRef } from "react"

const MyMesh = ({position, size, color}) => {
  const refMesh = useRef();

  useFrame((state, delta) => {
    if(refMesh.current) {
      refMesh.current.rotation.y += delta;
      refMesh.current.rotation.x += delta;
      refMesh.current.rotation.z += delta;
    }
  });
  return (
    <mesh position={position} ref={refMesh}>
      <boxGeometry args={size}/>
      <meshStandardMaterial color={color}/>
    </mesh>
    )
}

export default function Home() {
  return (
    <div>
      <main>
        <div className="px-8">
          <div className="grid max-w-screen-xl py-8 mx-auto lg:gap-8 xl:gap-0 lg:py-16 lg:grid-cols-12 lg:max-w-none lg:space-x-8 lg:items-center">
            <div className="mx-auto place-self-center lg:col-span-7">
              <motion.h1
                initial={{ x: 0, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ duration: 0.5 }}
                className="max-w-2xl mb-4 text-5xl font-bold tracking-tight leading-none md:text-5xl xl:text-6xl dark:text-white"
              >
                ssl<span className="text-primary">station</span>
              </motion.h1>
              <motion.p
                initial={{ x: 0, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 0.1, duration: 0.5 }}
                className="max-w-2xl mb-4 text-xl font-medium tracking-tight leading-none md:text-2xl xl:text-3xl dark:text-white"
              >
                the one stop station for your SSL hour needs.
              </motion.p>
              <motion.p
                initial={{ x: 0, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 0.2, duration: 0.5 }}
                className="max-w-2xl mb-6 font-light text-gray-500 lg:mb-8 md:text-lg lg:text-xl dark:text-gray-400"
              >
                Do you go to a Montgomery County Public School? Do you need more Student Service Learning hours for the 75 hour graduation requirement? Do you want the Certificate of Meritorious Service as an award for 240 SSL hours? Or, do you just want to be more connected to your community? SSL station is an app that refers to the MoCo Volunteer Center to help students create personalized and optimized schedules of SSL hour opportunities.
              </motion.p>
              <motion.p
                initial={{x:0, opacity:0}}
                animate={{x:0, opacity:1}}
                transition={{delay:0.4, duration:0.5}}
                className="max-w-2xl mb-6 font-light text-gray-500 lg:mb-8 md:text-lg lg:text-xl dark:text-gray-400"
              >
                SSL station is made by students, for students.
              </motion.p>
            </div>
            <div className="mx-auto hidden lg:mt-0 lg:col-span-5 lg:dark:block h-full">
              <Canvas>
                <directionalLight position={[0,0,2]} intensity={0.5}/>
                <ambientLight intensity={0.1}/>
                <MyMesh position={[0,0,0]} color="red" size={[2,2,2]}/>
              </Canvas>
            </div>
          </div>
        </div>
        <div className="bg-radial from-primary to-secondary">
          <svg 
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 1440 58" 
            className="top-0 bg-transparent w-full">
            <path 
              className="fill-background" 
              d="M-100 58C-100 58 218.416 36.3297 693.5 36.3297C1168.58 36.3297 1487 58 1487 58V-3.8147e-06H-100V58Z" >
            </path>
          </svg>
          <div className="grid grid-cols:9 text-background">
            <div className="mx-auto place-self-center lg:col-span3">
              <h1>
                Optimized Schedules
              </h1>
            </div>
            <div className="mx-auto place-self-center lg:col-span3">
              <h1>
                Routing to Opportunities
              </h1>
            </div>
            <div className="mx-auto place-self-center lg:col-span3">
              <h1>
                Personalized to your interests
              </h1>
            </div>
          </div>
          <svg 
            viewBox="0 0 1440 58" 
            xmlns="http://www.w3.org/2000/svg" 
            className="bottom-0 bg-transparent w-full">
            <path 
              className="fill-background"
              transform="rotate(180) translate(-1440, -60)" 
              d="M-100 58C-100 58 218.416 36.3297 693.5 36.3297C1168.58 36.3297 1487 58 1487 58V-3.8147e-06H-100V58Z">
            </path>
          </svg>
        </div>
      </main>
      <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center">
        <a 
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="https://github.com/danyul-h/ssl-station"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            className="dark:invert"
            aria-hidden
            src="/github-icon.svg"
            alt="Github icon"
            width={16}
            height={16}
          />
          Open Source
        </a>
      </footer>
    </div>
  );
}
