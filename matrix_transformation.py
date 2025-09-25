import numpy as np

def to_homogeneous(points_2d: np.ndarray) -> np.ndarray:
    ones = np.ones((points_2d.shape[0], 1))
    return np.hstack([points_2d, ones])

def from_homogeneous(points_3d: np.ndarray) -> np.ndarray:
    w = points_3d[:, 2:3]
    return points_3d[:, :2] / w

def apply_transform(points_2d: np.ndarray, T: np.ndarray) -> np.ndarray:
    P = to_homogeneous(points_2d)
    P2 = (T @ P.T).T
    return from_homogeneous(P2)

def T_translate(tx: float, ty: float) -> np.ndarray:
    T = np.eye(3); T[0,2]=tx; T[1,2]=ty; return T

def T_scale(sx: float, sy: float) -> np.ndarray:
    T = np.eye(3); T[0,0]=sx; T[1,1]=sy; return T

def T_rotate(theta_deg: float) -> np.ndarray:
    t = np.deg2rad(theta_deg); c, s = np.cos(t), np.sin(t)
    return np.array([[c,-s,0],[s,c,0],[0,0,1]], float)

def T_shear(kx: float = 0.0, ky: float = 0.0) -> np.ndarray:
    return np.array([[1,kx,0],[ky,1,0],[0,0,1]], float)

def T_about_point(Tlocal: np.ndarray, px: float, py: float) -> np.ndarray:
    return T_translate(px, py) @ Tlocal @ T_translate(-px, -py)
