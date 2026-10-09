import { useRef, useEffect, useMemo } from 'react'
import { useGLTF, useAnimations } from '@react-three/drei'
import * as THREE from 'three'
import { SkeletonUtils } from 'three-stdlib'

interface ModelProps {
  url: string;
  animationName?: string;
}

export function Model({ url, animationName }: ModelProps) {
  const group = useRef<THREE.Group>(null)
  const { scene, animations } = useGLTF(url)
  const clone = useMemo(() => SkeletonUtils.clone(scene), [scene])
  const { actions, names } = useAnimations(animations, group)

  useEffect(() => {
    const clipName = animationName ?? names[0]
    const action = actions[clipName]

    action?.reset().fadeIn(0.3).play()

    return () => {
      action?.fadeOut(0.3)
    }
  }, [actions, names, animationName])

  return <primitive ref={group} object={clone} scale={1} />
}